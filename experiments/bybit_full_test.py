import urllib.request, json, ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def test(name, url, payload=None, method='POST'):
    print("\n" + "="*50)
    print("Test:", name)
    print("="*50)
    try:
        if payload:
            data = json.dumps(payload).encode()
            req = urllib.request.Request(url, data=data, method=method)
            req.add_header('Content-Type', 'application/json')
        else:
            req = urllib.request.Request(url, method=method)
        req.add_header('User-Agent', 'Mozilla/5.0')
        req.add_header('Accept', 'application/json')
        r = urllib.request.urlopen(req, timeout=15, context=ctx)
        d = json.loads(r.read().decode())
        print("retCode:", d.get('retCode'))
        print("retMsg:", d.get('retMsg'))
        items = d.get('result', {}).get('items', [])
        print("Items:", len(items))
        if items:
            print("Keys:", list(items[0].keys())[:6])
            print("Sample:", {k: items[0].get(k) for k in ['nickName', 'price', 'lastQuantity'] if k in items[0]})
        return True
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, e.reason)
        return False
    except Exception as e:
        print("Error:", e)
        return False

test("Bybit NGN BUY", "https://api2.bybit.com/v5/p2p/item/online", {"tokenId":"USDT","currencyId":"NGN","side":"0","size":"10","page":"1"})
test("Bybit NGN SELL", "https://api2.bybit.com/v5/p2p/item/online", {"tokenId":"USDT","currencyId":"NGN","side":"1","size":"10","page":"1"})
test("Bybit USD BUY", "https://api2.bybit.com/v5/p2p/item/online", {"tokenId":"USDT","currencyId":"USD","side":"0","size":"10","page":"1"})
test("Bybit Market", "https://api.bybit.com/v5/market/tickers?category=spot&symbol=BTCUSDT", method='GET')

print("\nDONE")
