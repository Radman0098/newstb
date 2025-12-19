import sys
from pathlib import Path
import yaml
from src.utils.logger import setup_logger

config_path = Path('config/settings.yaml')
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

logger = setup_logger('Realistic_Test')
logger.info('Testing with realistic settings...')

try:
    from src.data.loader import DataLoader
    from src.features.atomic import AtomicFeatureExtractor
    from src.features.sequential import SequentialFeatureExtractor
    from src.features.topological import TopologicalFeatureExtractor
    from src.features.market_state import MarketStateEncoder
    from src.features.labeling import TripleBarrierLabeling
    from src.models.engine import ModelEngine
    from src.backtest.simulator import SimpleBacktest

    # Load data
    loader = DataLoader(raw_data_path='data/raw')
    data_map = loader.load_all(['M1'])
    df = data_map['M1'][:30000]  # Reasonable size

    logger.info(f'Original data: {len(df)} rows')

    # Feature extraction
    atomic = AtomicFeatureExtractor()
    df = atomic.process(df)

    seq = SequentialFeatureExtractor(window_size=10)
    df = seq.process(df)

    topo = TopologicalFeatureExtractor(phase_window=30, local_window=10, use_real_tda=False)
    df = topo.process(df)

    # Market state
    state_enc = MarketStateEncoder(n_clusters=4)
    split_idx = int(df.height * 0.6)
    state_enc.fit(df.slice(0, split_idx))
    df = state_enc.predict(df)

    # Labeling with new settings
    strat_cfg = config.get('strategy', {})
    tp_mult = float(strat_cfg.get('tp_mult', 2.0))
    sl_mult = float(strat_cfg.get('sl_mult', 1.0))
    time_limit = int(strat_cfg.get('time_limit', 30))

    labeler = TripleBarrierLabeling(tp_mult=tp_mult, sl_mult=sl_mult, time_limit=time_limit)
    df = labeler.apply(df)

    # Train/test split
    train_end = int(df.height * 0.75)  # 75% train, 25% test
    df_train = df.slice(0, train_end)
    df_test = df.slice(train_end, df.height - train_end)

    logger.info(f'Train: {len(df_train)} rows, Test: {len(df_test)} rows')

    # Train model
    engine = ModelEngine()
    engine.active_regimes = [0, 1, 2, 3]
    engine.train(df_train)

    # Generate signals with new threshold
    conf_threshold = float(strat_cfg.get('confidence_threshold', 0.4))
    df_signals = engine.generate_signals(df_test, threshold=conf_threshold)

    signal_counts = df_signals['signal'].value_counts()
    total_signals = (df_signals['signal'] != 0).sum()

    logger.info(f'Signals generated with threshold {conf_threshold}:')
    logger.info(f'  Total signals: {total_signals}')
    logger.info(f'  Distribution: {dict(zip(signal_counts["signal"].to_list(), signal_counts["count"].to_list()))}')

    if total_signals > 50:
        # Run backtest with realistic costs
        bt_cfg = config.get('backtest', {})

        results = SimpleBacktest.run(
            df_signals,
            tp_mult=tp_mult,
            sl_mult=sl_mult,
            time_limit=time_limit,
            spread=float(bt_cfg.get('spread', 0.2)),
            commission=float(bt_cfg.get('commission', 0.001)),
            slippage=float(bt_cfg.get('slippage', 0.002)),
            initial_capital=float(bt_cfg.get('initial_capital', 100.0)),
            risk_per_trade=0.02,
            use_conf_sizing=True,
            max_dd_stop_pct=50.0,  # Allow realistic DD
            use_kelly=True,
            kelly_fraction=0.25,
            use_partial_tp=True,
            partial_tp_levels=[0.5, 0.3, 0.2],
            use_dynamic_risk=True,
            dynamic_risk_window=20,
            use_volatility_sizing=True,
            vol_lookback=20
        )

        logger.info('\n=== REALISTIC BACKTEST RESULTS ===')
        logger.info(f'Total Trades: {results.get("Total Trades", 0)}')
        logger.info(f'Wins: {results.get("Wins", 0)}')
        logger.info(f'Losses: {results.get("Losses", 0)}')
        logger.info(f'Win Rate: {results.get("Win Rate", 0):.3f}')
        logger.info(f'Profit Factor: {results.get("Profit Factor", 0):.3f}')
        logger.info(f'Total R: {results.get("Total R", 0):.3f}')
        logger.info(f'Return %: {results.get("Return %", 0):.3f}')
        logger.info(f'Max DD %: {results.get("Max DD %", 0):.3f}')
        logger.info(f'Final Equity: ${results.get("Final Equity", 0):.2f}')
        logger.info(f'Sharpe Ratio: {results.get("Sharpe Ratio", 0):.3f}')

        # Risk analysis
        max_dd = results.get('Max DD %', 0)
        total_r = results.get('Total R', 0)
        win_rate = results.get('Win Rate', 0)

        logger.info('\n=== RISK ANALYSIS ===')
        if max_dd > 20:
            logger.warning('High drawdown - consider risk management improvements')
        elif max_dd < 5:
            logger.warning('Very low drawdown - possible overfitting or insufficient trades')
        else:
            logger.info('Reasonable drawdown levels')

        if total_r > 10 and max_dd < 15:
            logger.info('Good risk-adjusted returns!')
        elif total_r < 2:
            logger.warning('Poor returns - model needs improvement')

        if win_rate > 0.6 and max_dd > 10:
            logger.warning('High win rate with significant DD - check for curve fitting')

    else:
        logger.warning('Not enough signals generated - adjust threshold or check model')

    logger.info('\nRealistic testing complete!')

except Exception as e:
    logger.error(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()
