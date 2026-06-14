import requests

BOT_TOKEN = "8517898625:AAEZmk1kSNm82PihpmudLtaRtO6xpRUqw5E"
CHAT_ID = "7588696401"

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": msg
        }
    )

def get_btc_price():
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

        data = requests.get(url, timeout=10).json()

        if "price" in data:
            return float(data["price"])

        return None

    except:
        return None


def structure_analysis(price):
    swing_high = price * 1.01
    swing_low = price * 0.99

    range_size = swing_high - swing_low

    fib_618 = swing_high - (0.618 * range_size)
    fib_382 = swing_high - (0.382 * range_size)

    return {
        "high": swing_high,
        "low": swing_low,
        "fib618": fib_618,
        "fib382": fib_382
    }


def analyze(price):

    s = structure_analysis(price)

    # Simple trend approximation
    trend_up = price > ((s["high"] + s["low"]) / 2)

    # Simple liquidity zones
    liquidity_high = s["high"]
    liquidity_low = s["low"]

    if trend_up and price <= s["fib618"]:

        return {
            "direction": "BUY",
            "entry": price,
            "tp": liquidity_high,
            "sl": liquidity_low
        }

    if (not trend_up) and price >= s["fib382"]:

        return {
            "direction": "SELL",
            "entry": price,
            "tp": liquidity_low,
            "sl": liquidity_high
        }

    return None


price = get_btc_price()

if price is None:
    send("⚠️ Could not get BTC market data")
    raise SystemExit()

signal = analyze(price)

if signal:

    send(
f"""📊 V6 SCANNER

Asset: BTCUSD

Direction: {signal['direction']}

Entry: {round(signal['entry'],2)}
TP: {round(signal['tp'],2)}
SL: {round(signal['sl'],2)}

Structure: Enabled
Liquidity Zones: Enabled
"""
    )

else:
    send("📊 V6: No setup found")
