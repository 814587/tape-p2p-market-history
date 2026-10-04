import sqlite3, json, time, sys
from datetime import datetime
import requests

URL = "https://api2.bybit.com/fiat/otc/item/online"
HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36"
}
DB = "tape_test.db"
TOKENS = ["BTC", "ETH", "USDT"]
SIDES = [("1", "sell ads / Buy tab"), ("0", "buy ads / Sell tab")]

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS market_snapshots(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT, token TEXT, side TEXT, status TEXT,
        best REAL, avg REAL, ad_count INTEGER, error TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS prices(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        snapshot_id INTEGER, ts TEXT, token TEXT, side TEXT,
        price REAL, min_amount TEXT, max_amount TEXT,
        quantity TEXT, payments TEXT, seller TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS raw_ads(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        snapshot_id INTEGER, ts TEXT, token TEXT, side TEXT, json TEXT)""")
    conn.commit()
    return conn

def fetch_ads(token, side, attempts=4):
    payload = {
        "userId": "", "tokenId": token, "currencyId": "NGN",
        "payment": [], "side": side, "size": "10", "page": "1",
        "amount": "", "authMaker": False, "canTrade": False, "itemRegion": 1
    }
    delay = 5
    for attempt in range(1, attempts + 1):
        try:
            r = requests.post(URL, json=payload, headers=HEADERS, timeout=(10, 25))
            data = r.json()
            if data.get("ret_code") == 0:
                return data.get("result", {}).get("items", [])
            last_err = f"ret_code={data.get('ret_code')}"
        except Exception as e:
            last_err = str(e)
        print(f"  retry {attempt}/{attempts} in {delay}s ({last_err[:60]})")
        time.sleep(delay)
        delay *= 2
    return None

def snap(conn, token, side, side_label):
    ts = datetime.now().isoformat(timespec="seconds")
    ads = fetch_ads(token, side)
    c = conn.cursor()
    if ads is None:
        c.execute("INSERT INTO market_snapshots(ts,token,side,status,error) VALUES(?,?,?,?,?)",
                  (ts, token, side_label, "failed", "timeout after retries"))
        conn.commit()
        print(f"{token} | {side_label} | FAILED (recorded)")
        return
    c.execute("INSERT INTO market_snapshots(ts,token,side,status,best,avg,ad_count) VALUES(?,?,?,?,?,?,?)",
              (ts, token, side_label, "ok", None, None, 0))
    snap_id = c.lastrowid
    prices = []
    for a in ads:
        price = float(a.get("price") or 0)
        prices.append(price)
        pays = a.get("payment", [])
        pay_names = ",".join(str(p.get("name", p)) if isinstance(p, dict) else str(p) for p in pays)
        c.execute("""INSERT INTO prices(snapshot_id,ts,token,side,price,min_amount,max_amount,quantity,payments,seller)
                     VALUES(?,?,?,?,?,?,?,?,?,?)""",
                  (snap_id, ts, token, side_label, price,
                   str(a.get("minAmount", "")), str(a.get("maxAmount", "")),
                   str(a.get("quantity", "")), pay_names, a.get("nickName", "")))
        c.execute("INSERT INTO raw_ads(snapshot_id,ts,token,side,json) VALUES(?,?,?,?,?)",
                  (snap_id, ts, token, side_label, json.dumps(a)))
    if prices:
        best = min(prices); avg = sum(prices) / len(prices)
        c.execute("UPDATE market_snapshots SET best=?, avg=?, ad_count=? WHERE id=?",
                  (best, avg, len(prices), snap_id))
        print(f"{token} | {side_label} | best={best:,.2f} avg={avg:,.2f} ads={len(prices)} -> saved #{snap_id}")
    else:
        print(f"{token} | {side_label} | NO ADS -> saved #{snap_id}")
    conn.commit()

def main():
    conn = init_db()
    loop_min = 0
    if "--loop" in sys.argv:
        loop_min = int(sys.argv[sys.argv.index("--loop") + 1])
    while True:
        print(f"\n=== TAPE RUN {datetime.now():%Y-%m-%d %H:%M:%S} ===")
        for token in TOKENS:
            for side, label in SIDES:
                snap(conn, token, side, f"side {side} ({label})")
                time.sleep(3)
        if not loop_min:
            break
        print(f"sleeping {loop_min} min...")
        time.sleep(loop_min * 60)

main()
