import sys
import os
from pathlib import Path
import time
import logging

# Add project root to path
sys.path.append(os.getcwd())
from src.execution.mt5_bridge import MT5Bridge

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BridgeTest")

def run_test():
    print("--- Starting Bridge Test ---")
    
    try:
        # 1. Initialize Bridge (Auto-detect path)
        print("Initializing Bridge...")
        bridge = MT5Bridge()
        
        if not bridge.base_path:
            print("ERROR: Could not auto-detect MT5 path.")
            return

        print(f"Bridge initialized. Path: {bridge.base_path}")
        
        if not bridge.connect():
            print("ERROR: Could not write to shared folder.")
            return

        # 2. Test Market Data Stream
        print("\n[Test 1] Reading Market Stream...")
        # Try a few common symbols if XAUUSD is not open
        symbols = ["XAUUSD", "EURUSD", "GBPUSD", "BTCUSD"]
        price = None
        for sym in symbols:
            p = bridge.get_current_price(sym)
            if p:
                price = p
                print(f"SUCCESS: Received Tick Data for {sym}: {price}")
                break
        
        if not price:
            print("WARNING: No live tick data found yet (Ensure EA is running on a chart).")

        # 3. Test Command: Get History
        print("\n[Test 2] Requesting History (M1)...")
        # Use the symbol we found, or default
        target_sym = "XAUUSD"
        df = bridge.get_market_data(target_sym, "M1", n_candles=10)
        if df is not None and len(df) > 0:
            print(f"SUCCESS: Received {len(df)} candles.")
            print(df.head(3))
        else:
            print("FAILURE: Could not retrieve history.")
        
    except Exception as e:
        print(f"EXCEPTION: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_test()
