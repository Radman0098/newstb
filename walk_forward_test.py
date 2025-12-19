import sys
from pathlib import Path
import yaml
from src.utils.logger import setup_logger
from sklearn.model_selection import TimeSeriesSplit
import numpy as np

config_path = Path('config/settings.yaml')
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

logger = setup_logger('Walk_Forward_Test')
logger.info('Running Walk-Forward Validation for realistic performance assessment...')

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
    df = data_map['M1'][:40000]  # Larger sample for better validation

    logger.info(f'Total data: {len(df)} rows')

    # Feature extraction
    atomic = AtomicFeatureExtractor()
    df = atomic.process(df)

    seq = SequentialFeatureExtractor(window_size=10)
    df = seq.process(df)

    topo = TopologicalFeatureExtractor(phase_window=30, local_window=10, use_real_tda=False)
    df = topo.process(df)

    # Market state
    state_enc = MarketStateEncoder(n_clusters=4)
    split_idx = int(df.height * 0.5)  # Use first 50% for training market states
    state_enc.fit(df.slice(0, split_idx))
    df = state_enc.predict(df)

    # Labeling with conservative settings
    strat_cfg = config.get('strategy', {})
    tp_mult = float(strat_cfg.get('tp_mult', 1.5))
    sl_mult = float(strat_cfg.get('sl_mult', 0.8))
    time_limit = int(strat_cfg.get('time_limit', 20))

    labeler = TripleBarrierLabeling(tp_mult=tp_mult, sl_mult=sl_mult, time_limit=time_limit)
    df = labeler.apply(df)

    logger.info(f'Final data shape: {df.shape}')

    # Walk-forward validation
    tscv = TimeSeriesSplit(n_splits=5, test_size=int(df.height * 0.15))  # 15% test each fold

    wf_results = []

    for fold, (train_idx, test_idx) in enumerate(tscv.split(df)):
        logger.info(f'\n--- Walk-Forward Fold {fold + 1} ---')

        # Split data
        df_train = df.slice(train_idx[0], len(train_idx))
        df_test = df.slice(test_idx[0], len(test_idx))

        # Retrain market state encoder on training data
        state_enc_fold = MarketStateEncoder(n_clusters=4)
        state_enc_fold.fit(df_train)
        df_train = state_enc_fold.predict(df_train)
        df_test = state_enc_fold.predict(df_test)

        logger.info(f'Fold {fold + 1}: Train={len(df_train)}, Test={len(df_test)}')

        # Train model
        engine = ModelEngine()
        engine.active_regimes = [0, 1, 2, 3]
        engine.train(df_train)

        # Generate signals
        conf_threshold = float(strat_cfg.get('confidence_threshold', 0.5))
        df_signals = engine.generate_signals(df_test, threshold=conf_threshold)

        total_signals = (df_signals['signal'] != 0).sum()
        logger.info(f'Signals in fold {fold + 1}: {total_signals}')

        if total_signals > 20:  # Minimum trades for meaningful results
            # Run backtest
            bt_cfg = config.get('backtest', {})

            results = SimpleBacktest.run(
                df_signals,
                tp_mult=tp_mult,
                sl_mult=sl_mult,
                time_limit=time_limit,
                spread=float(bt_cfg.get('spread', 0.5)),
                commission=float(bt_cfg.get('commission', 0.002)),
                slippage=float(bt_cfg.get('slippage', 0.005)),
                initial_capital=float(bt_cfg.get('initial_capital', 100.0)),
                risk_per_trade=0.02,
                use_conf_sizing=True,
                max_dd_stop_pct=50.0
            )

            fold_result = {
                'fold': fold + 1,
                'trades': results.get('Total Trades', 0),
                'win_rate': results.get('Win Rate', 0),
                'total_r': results.get('Total R', 0),
                'max_dd': results.get('Max DD %', 0),
                'return_pct': results.get('Return %', 0),
                'sharpe': results.get('Sharpe Ratio', 0)
            }

            wf_results.append(fold_result)

            logger.info(f'Fold {fold + 1} Results:')
            logger.info(f'  Trades: {fold_result["trades"]}')
            logger.info(f'  Win Rate: {fold_result["win_rate"]:.3f}')
            logger.info(f'  Total R: {fold_result["total_r"]:.3f}')
            logger.info(f'  Max DD: {fold_result["max_dd"]:.3f}%')
            logger.info(f'  Return: {fold_result["return_pct"]:.3f}%')
            logger.info(f'  Sharpe: {fold_result["sharpe"]:.3f}')

    # Summary
    if wf_results:
        logger.info('\n' + '='*50)
        logger.info('WALK-FORWARD VALIDATION SUMMARY')
        logger.info('='*50)

        win_rates = [r['win_rate'] for r in wf_results]
        total_rs = [r['total_r'] for r in wf_results]
        max_dds = [r['max_dd'] for r in wf_results]
        returns = [r['return_pct'] for r in wf_results]
        sharpes = [r['sharpe'] for r in wf_results]

        logger.info(f'Number of folds: {len(wf_results)}')
        logger.info(f'Average Win Rate: {np.mean(win_rates):.3f} ± {np.std(win_rates):.3f}')
        logger.info(f'Average Total R: {np.mean(total_rs):.3f} ± {np.std(total_rs):.3f}')
        logger.info(f'Average Max DD: {np.mean(max_dds):.3f}% ± {np.std(max_dds):.3f}%')
        logger.info(f'Average Return: {np.mean(returns):.3f}% ± {np.std(returns):.3f}%')
        logger.info(f'Average Sharpe: {np.mean(sharpes):.3f} ± {np.std(sharpes):.3f}')

        # Overall assessment
        avg_win_rate = np.mean(win_rates)
        avg_max_dd = np.mean(max_dds)
        avg_total_r = np.mean(total_rs)

        logger.info('\nOVERALL ASSESSMENT:')
        if avg_win_rate > 0.55 and avg_max_dd < 10 and avg_total_r > 5:
            logger.info('✅ EXCELLENT: Model shows strong generalization with realistic risk metrics')
        elif avg_win_rate > 0.52 and avg_max_dd < 15:
            logger.info('✅ GOOD: Model performs well with acceptable risk levels')
        elif avg_max_dd > 20:
            logger.warning('⚠️ HIGH RISK: Model shows concerning drawdown levels')
        else:
            logger.info('🤔 MODERATE: Model shows some promise but needs improvement')

        # Check for overfitting
        if np.std(total_rs) > np.mean(total_rs) * 0.8:
            logger.warning('🚨 OVERFITTING DETECTED: High variance across folds')
        else:
            logger.info('✅ CONSISTENT: Results are stable across time periods')

    logger.info('\nWalk-forward validation complete!')

except Exception as e:
    logger.error(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()
