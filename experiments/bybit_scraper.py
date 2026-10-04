import requests
import json
from datetime import datetime, timezone

def get_bybit_p2p_ads(token="USDT", currency="NGN", side="1"):
    url = "https://api.bybit.com/v5/p2p/item/online"
    payload = {
        "tokenId": token,
        "currencyId": currency,
        "side": side,
        "size": "10",
        "page": "1",
        "amount": "",
        "payment": [],
        "orderType": "0"
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    if data.get("retCode") == 0:
        return data["result"]["items"]
    else:
        print(f"Error: {data.get('retMsg')}")
        return []

def get_best_prices(token="USDT", currency="NGN"):
    buy_ads = get_bybit_p2p_ads(token, currency, side="0")
    best_bid = float(buy_ads[0]["price"]) if buy_ads else None
    sell_ads = get_bybit_p2p_ads(token, currency, side="1")
    best_ask = float(sell_ads[0]["price"]) if sell_ads else None
    return best_bid, best_ask

def calculate_spread(bid, ask):
    if not bid or not ask:
        return None
    gap = ask - bid
    midpoint = (ask + bid) / 2
    spread_pct = (gap / midpoint) * 100
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "bid": bid,
        "ask": ask,
        "gap": gap,
        "midpoint": midpoint,
        "spread_pct": round(spread_pct, 4)
    }

if __name__ == "__main__":
    bid, ask = get_best_prices("USDT", "NGN")
    if bid and ask:
        result = calculate_spread(bid, ask)
        print(json.dumps(result, indent=2))
    else:
        print("Failed to fetch prices")
