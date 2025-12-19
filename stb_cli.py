import sys


def _print_help() -> None:
    print(
        """STB Unified CLI

Usage:
  python3 stb_cli.py <command> [args]

Commands:
  train           Train/backtest pipeline (wraps src.app.train_app)
  live            Live trading loop (wraps src.app.live_app)
  tune            Random-search tuner (wraps src.app.tune)
  learn           Offline learning from MT5 history (wraps scripts/learn_from_failures.py)
  analyze         Offline failure anatomy analysis (wraps scripts/analyze_errors.py)
  export-history  Export MT5 deal history to CSV (via MT5Bridge)

Examples:
  python3 stb_cli.py live --config config/settings.hybrid.tuned.yaml --timeframe M1 --live --confirm-live --learn
  python3 stb_cli.py train --config config/settings.hybrid.tuned.yaml
  python3 stb_cli.py tune --config config/settings.hybrid.tuned.yaml --symbol XAUUSD --trials 50
  python3 stb_cli.py export-history --days 90 --only-ours 1
"""
    )


def main(argv: list[str] | None = None) -> None:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("-h", "--help"):
        _print_help()
        return

    cmd = argv[0]
    sub_argv = argv[1:]

    if cmd == "train" or cmd == "backtest":
        from src.app.train_app import main as train_main

        train_main(sub_argv)
        return

    if cmd == "live":
        from src.app.live_app import main as live_main

        live_main(sub_argv)
        return

    if cmd == "tune":
        from src.app.tune import main as tune_main

        tune_main(sub_argv)
        return

    if cmd == "learn":
        # Offline learner (full history mode)
        from scripts.learn_from_failures import main as learn_main

        learn_main()
        return

    if cmd == "analyze":
        from scripts.analyze_errors import main as analyze_main

        analyze_main()
        return

    if cmd == "export-history":
        import argparse

        ap = argparse.ArgumentParser()
        ap.add_argument("--days", type=int, default=90)
        ap.add_argument("--only-ours", type=int, default=1)
        ap.add_argument("--mt5-path", type=str, default="")
        args = ap.parse_args(sub_argv)

        from src.execution.mt5_bridge import MT5Bridge

        bridge = MT5Bridge(mt5_data_path=args.mt5_path or None)
        df = bridge.export_trade_history(days=int(args.days), only_ours=bool(int(args.only_ours)))
        if df is None:
            raise SystemExit("Failed exporting history")
        print(df.tail(5))
        return

    print(f"Unknown command: {cmd}\n")
    _print_help()


if __name__ == "__main__":
    main()
