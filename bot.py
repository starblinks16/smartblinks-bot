def requests

BOT_TOKEN = "8517898625:AAEZmk1kSNm82PihpmudLtaRtO6xpRUqw5E"
CHAT_ID = "7588696401"

# ---------------------------
# GET REAL BTC PRICE (FREE)
# ---------------------------
def get_btc_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    response = requests.get(url)
    data = response.json()

    # SAFETY CHECK (THIS FIXES YOUR ERROR)
    if "price" not in data:
        print("API ERROR:", data)
        return None

    return float(data["price"])

# ---------------------------
# FIBONACCI LOGIC (REALISTIC SIMPLE MODEL)
# ---------------------------
def fibonacci_signal(price):
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

# ---------------------------
# TELEGRAM SENDER
# ---------------------------
def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

# ---------------------------
# MAIN EXECUTION
# ----------------------------price = get_btc_price()

if price is None:
    send("⚠️ Failed to get market data")
    exit()ceif signal:
    direction, entry, tp, sl = signal

    message = f"""
📊 BTC SIGNAL (FIBONACCI BOT)

Direction: {direction}
Entry: {round(entry, 2)}
TP: {round(tp, 2)}
SL: {round(sl, 2)}

Price: {round(price, 2)}
"""

    send(message)
else:
    send("📊 No valid Fibonacci signal right now")
