import sys
import os
import time
import logging
import yaml
import polars as pl
import numpy as np
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.append(".")
from src.models.engine import ModelEngine
from src.features.atomic import AtomicFeatureExtractor
from src.features.sequential import SequentialFeatureExtractor
from src.features.topological import TopologicalFeatureExtractor
from src.features.market_state import MarketStateEncoder
from src.execution.mt5_bridge import MT5Bridge

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("live_trading.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("LiveTrader")

def load_config(config_path: str = "config/settings.yaml") -> dict:
    if not os.path.exists(config_path):
        return {}
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def main():
    logger.info("Starting UltraMax Live Trading System (Multi-Position Mode)...")
    
    # 1. Load Config & Initialize
    config = load_config()
    strategy_cfg = config.get("strategy", {})
    
    symbol = str(config.get("data", {}).get("symbol", "XAUUSD"))
    timeframe = "M1"
    
    # Multi-position settings
    max_positions = int(strategy_cfg.get("max_open_positions", 3))  # Allow up to 3 positions by default
    min_dist_pips = float(strategy_cfg.get("stacking_min_dist", 10.0)) # Don't stack too close
    
    # Initialize Engine (Loads trained models)
    engine = ModelEngine(config=config, persist_models=False) # Read-only mode for models
    
    # Load all sub-models
    logger.info("Loading Models...")
    if not engine.load_metadata():
        logger.error("Failed to load model metadata. Please train the system first.")
        return

    engine.load_xgb_models()
    engine.load_lstm()
    engine.load_patchtst()
    engine.load_memory_banks()
    
    # Initialize Feature Extractors
    atomic_extractor = AtomicFeatureExtractor()
    seq_extractor = SequentialFeatureExtractor(window_size=10)
    topo_extractor = TopologicalFeatureExtractor(phase_window=60, local_window=20)
    
    # Initialize Bridge
    bridge = MT5Bridge()
    if not bridge.base_path:
        logger.error("MT5 Data path not found.")
        return
        
    logger.info(f"Bridge connected to: {bridge.base_path}")
    
    # Trading Loop Variables
    last_candle_time = 0
    buffer_size = 500 
    
    logger.info(f"Entering Trading Loop for {symbol} {timeframe} (Max Pos: {max_positions})...")
    
    while True:
        try:
            # 1. Wait for New Candle (or check every X seconds)
            time.sleep(1) 
            
            # Get latest market data
            df_hist = bridge.get_market_data(symbol, timeframe, n_candles=buffer_size)
            
            if df_hist is None or df_hist.height < 100:
                logger.warning("Insufficient history data received.")
                time.sleep(5)
                continue
                
            # Check for new closed candle
            last_closed_idx = df_hist.height - 2
            if last_closed_idx < 0: continue
            
            closed_candle_time = df_hist["Time"][last_closed_idx]
            
            if closed_candle_time == last_candle_time:
                continue
                
            last_candle_time = closed_candle_time
            logger.info(f"New Candle Detected: {closed_candle_time}")
            
            # 2. Feature Extraction
            df_feats = df_hist.clone()
            df_feats = atomic_extractor.process(df_feats)
            df_feats = seq_extractor.process(df_feats)
            df_feats = topo_extractor.process(df_feats)
            
            # Market State (Fallback heuristic if HMM not loaded)
            if "market_state" not in df_feats.columns:
                vol = df_feats["vol_10"]
                q33 = vol.quantile(0.33)
                q66 = vol.quantile(0.66)
                states = pl.when(vol < q33).then(0).when(vol < q66).then(1).otherwise(2)
                df_feats = df_feats.with_columns(states.alias("market_state"))

            # 3. Generate Signal
            df_signals = engine.generate_hybrid_signals(
                df_feats.tail(200),
                threshold=0.60 
            )
            
            last_row = df_signals.row(-1, named=True)
            signal = last_row["signal"]
            conf = last_row.get("signal_conf", 0.0)
            
            logger.info(f"Signal Analysis: Dir={signal} Conf={conf:.4f} State={last_row['market_state']}")
            
            # 4. Execute Trade (Smart Stacking Logic)
            if signal != 0:
                action = "BUY" if signal == 1 else "SELL"
                
                # Get current positions
                positions = bridge.get_positions(symbol)
                current_count = len(positions) if positions else 0
                
                # Check 1: Max Position Count
                if current_count >= max_positions:
                    logger.info(f"Max positions reached ({current_count}/{max_positions}). Skipping.")
                    continue
                    
                # Check 2: Stacking Distance (Don't open new trade if price is too close to existing ones)
                # This prevents opening 5 trades at the exact same price during a choppy minute.
                too_close = False
                current_price = bridge.get_current_price(symbol)
                if current_price and positions:
                    bid = current_price['bid']
                    ask = current_price['ask']
                    entry_price = ask if action == "BUY" else bid
                    point = 0.01 # Approximate, should get from symbol info
                    
                    for pos in positions:
                        # Only check same-direction trades
                        pos_type = "BUY" if pos['type'] == 0 else "SELL"
                        if pos_type == action:
                            dist = abs(entry_price - pos['price_open'])
                            # Assuming standard forex pair or gold, need symbol info for precise pip calc
                            # Heuristic: if dist is very small (< min_dist_pips * point)
                            # For XAUUSD, 1 pip = 0.1 usually.
                            if dist < 0.5: # Example hardcoded safety distance
                                too_close = True
                                break
                
                if too_close:
                    logger.info("Price too close to existing position. Skipping stacking.")
                    continue

                # Execute
                logger.info(f"*** EXECUTING {action} (Pos {current_count + 1}/{max_positions}) ***")
                
                snapshot = {k: v for k, v in last_row.items() if isinstance(v, (int, float, str, bool))}
                
                # Dynamic Volume Sizing based on Confidence?
                # Base vol = 0.01. If Conf > 0.8, maybe 0.02?
                vol = 0.01
                if conf > 0.80: vol = 0.02
                
                res = bridge.execute_trade(
                    symbol=symbol, 
                    action=action, 
                    volume=vol, 
                    sl=0.0, 
                    tp=0.0,
                    snapshot=snapshot
                )
                
                if res["retcode"] == 0:
                    logger.info(f"Trade Success: Order {res.get('order')}")
                else:
                    logger.error(f"Trade Failed: {res.get('comment')}")
            
        except KeyboardInterrupt:
            logger.info("Stopping Live Trader...")
            break
        except Exception as e:
            logger.error(f"Error in main loop: {e}", exc_info=True)
            time.sleep(5)

if __name__ == "__main__":
    import os
    main()
