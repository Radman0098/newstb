import sys
import time
from src.execution.mt5_bridge import MT5Bridge

def test_bridge():
    print("--- Testing Python <-> MT5 Bridge ---")
    
    try:
        # 1. Initialize Bridge (Auto-detect path)
        bridge = MT5Bridge()
        print(f"[OK] Bridge initialized. Base path: {bridge.base_path}")
        
        # 2. Check Connection Write Access
        if bridge.connect():
            print("[OK] Connection test successful (Write access confirmed)")
        else:
            print("[FAIL] Cannot write to shared folder.")
            return

        # 3. Read Market Data (Heartbeat from EA)
        print("Waiting for heartbeat from EA (stb_market.txt)...")
        tick = None
        for i in range(10): # Try 10 times
            tick = bridge.get_current_price("XAUUSD") # Or whatever symbol is active
            # Try generic read if symbol mismatch
            if not tick:
                # Direct read
                mkt_path = bridge.base_path / "stb_market.txt"
                if mkt_path.exists():
                    with open(mkt_path, "r") as f:
                        print(f"   [RAW] Market File Content: {f.read().strip()}")
                    break
            else:
                print(f"[OK] Received Tick: {tick}")
                break
            time.sleep(1)
            
        if not tick and not (bridge.base_path / "stb_market.txt").exists():
            print("[WARN] No market data received yet. Is the EA running on a chart?")
        
        print("\n--- Test Complete ---")
        
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    test_bridge()
