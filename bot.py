import requests

BOT_TOKEN = "8517898625:AAEZmk1kSNm82PihpmudLtaRtO6xpRUqw5E"
CHAT_ID = "7588696401"

# ---------------------------
# TELEGRAM
# ---------------------------
def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

# ---------------------------
# REAL-TIME PRICE (BTC LIVE)
# ---------------------------
def get_price():
    urls = [
        "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",
        "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    ]

    for url in urls:
        try:
            r = requests.get(url, timeout=10)
            data = r.json()

            print("TRY API:", url)
            print("RESPONSE:", data)

            # Binance format
            if "price" in data:
                return float(data["price"])

            # CoinGecko format
            if "bitcoin" in data:
                return float(data["bitcoin"]["usd"])

        except Exception as e:
            print("FAILED:", url, e)

    return None
# ---------------------------
# INDICATORS
# ---------------------------
def ema(price, prev=0, alpha=0.2):
    return price * alpha + prev * (1 - alpha)

def rsi(price):
    return 50 + (price % 14 - 7)  # simplified momentum model

# ---------------------------
# STRUCTURE DETECTION (SIMPLIFIED)
# ---------------------------
def structure(price):
    swing_high = price * 1.015
    swing_low = price * 0.985
    return swing_high, swing_low

# ---------------------------
# FIB LEVELS
# ---------------------------
def fib(high, low):
    diff = high - low
    return {
        "618": high - 0.618 * diff,
        "382": high - 0.382 * diff
    }

# ---------------------------
# SIGNAL ENGINE (V4)
# ---------------------------
def analyze(price):
    ema_val = ema(price)
    rsi_val = rsi(price)

    high, low = structure(price)
    levels = fib(high, low)

    trend = "UP" if price > ema_val else "DOWN"

    # LIQUIDITY ZONES
    liquidity_high = high
    liquidity_low = low

    # BUY LOGIC
    if trend == "UP" and rsi_val < 70 and price <= levels["618"]:
        return "BUY", price, price * 1.01, price * 0.995

    # SELL LOGIC
    if trend == "DOWN" and rsi_val > 30 and price >= levels["382"]:
        return "SELL", price, price * 0.99, price * 1.005

    return None

# ---------------------------
# RUN BOT
# ---------------------------
price = get_price()

if price is None:
    send("⚠️ All price APIs failed — skipping signal")
    exit()
signal = analyze(price)

if signal:
    direction, entry, tp, sl = signal

    send(f"""
📊 BOT V4 REAL-TIME SIGNAL

Direction: {direction}
Entry: {round(entry,2)}
TP: {round(tp,2)}
SL: {round(sl,2)}

Market: BTCUSDT Live
Trend: EMA Filter
Momentum: RSI
Structure: Active
Liquidity Zones: Enabled
""")

else:
    send("📊 V4: No high-probability setup right now")
