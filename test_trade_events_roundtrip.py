import time
from pathlib import Path

from src.execution.mt5_bridge import MT5Bridge


def main():
    b = MT5Bridge()
    print(f"MT5 Files path: {b.base_path}")

    # Sanity: ping-like call
    acct = b.get_account_info()
    print("Account:", acct)

    sym = "XAUUSD"
    # Try opening and closing a tiny position to force a DEAL_ENTRY_OUT event.
    # WARNING: This is a real trade if AlgoTrading is on. Prefer DEMO.
    tick = b.get_current_price(sym)
    print("Tick:", tick)

    # Open BUY 0.01 without SL/TP (we will close immediately)
    snap = {"purpose": "trade_events_roundtrip"}
    r = b.execute_trade(sym, "BUY", 0.01, sl=0.0, tp=0.0, snapshot=snap)
    print("Open result:", r)

    if r.get("retcode") != 0:
        print("Open failed; abort.")
        return

    # Wait a bit for MT5 to register the position
    time.sleep(2)

    pos = b.get_positions(sym) or []
    ours = [p for p in pos if int(p.get("magic", 0) or 0) == 234000]
    print(f"Positions total={len(pos)} ours={len(ours)}")
    if not ours:
        print("No position found to close.")
        return

    ticket = int(ours[-1]["ticket"])
    ok = b.close_position(ticket)
    print("Close sent:", ok, "ticket=", ticket)

    # Wait for OnTradeTransaction + file write
    events_path = b.base_path / "stb_trade_events.csv"
    for i in range(20):
        if events_path.exists() and events_path.stat().st_size > 0:
            print("Trade events file exists:", events_path)
            print(events_path.read_text(encoding="utf-8", errors="ignore")[-500:])
            return
        time.sleep(0.5)

    print("Trade events file still not created.")


if __name__ == "__main__":
    main()
