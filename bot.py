import requests

BOT_TOKEN = "8517898625:AAEZmk1kSNm82PihpmudLtaRtO6xpRUqw5E"
CHAT_ID = "7588696401"

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def get_price():
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        r = requests.get(url, timeout=10)
        data = r.json()

        print("RAW API RESPONSE:", data)

        if "price" in data:
            return float(data["price"])

        return None

    except Exception as e:
        print("PRICE ERROR:", e)
        return None

def fibonacci(price):
    high = price * 1.01
    low = price * 0.99
    diff = high - low

    fib_618 = high - 0.618 * diff
    fib_382 = high - 0.382 * diff

    if price <= fib_618:
        return "BUY", price, price + diff*0.5, price - diff*0.3

    if price >= fib_382:
        return "SELL", price, price - diff*0.5, price + diff*0.3

    return None

send("🤖 Bot Started Successfully")

price = get_price()

# fallback so bot NEVER breaks
if price is None:
    price = 65000  # fallback BTC estimate
    send("⚠️ Using fallback price (API unstable)")
    signal = fibonacci(price)

    if signal:
        direction, entry, tp, sl = signal

        send(f"""
📊 BTC SIGNAL

Direction: {direction}
Entry: {round(entry,2)}
TP: {round(tp,2)}
SL: {round(sl,2)}

Price: {round(price,2)}
""")
    else:
        send("📊 No valid Fibonacci signal right now")
