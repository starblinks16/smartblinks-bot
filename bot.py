import requests

BOT_TOKEN = "8517898625:AAEZmk1kSNm82PihpmudLtaRtO6xpRUqw5E"
CHAT_ID = "7588696401"

# -------------------------
# TELEGRAM
# -------------------------
def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

# -------------------------
# MARKET DATA
# -------------------------
def get_price(symbol):
    try:
        if symbol == "BTCUSD":
            url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
            data = requests.get(url, timeout=10).json()
            return float(data["price"])

        # simulated forex/gold (free limitation)
        if symbol == "EURUSD":
            return 1.08
        if symbol == "XAUUSD":
            return 2025

    except:
        return None

# -------------------------
# INDICATORS
# -------------------------
def ema_score(price):
    return price / 100  # simplified trend proxy

def rsi_score(price):
    return 50 + (price % 10 - 5)

# -------------------------
# STRUCTURE + FIB
# -------------------------
def analyze(symbol, price):
    high = price * 1.01
    low = price * 0.99
    diff = high - low

    fib_618 = high - 0.618 * diff
    fib_382 = high - 0.382 * diff

    ema = ema_score(price)
    rsi = rsi_score(price)

    trend_up = price > ema

    score = 0

    # Trend
    if trend_up:
        score += 2
    else:
        score -= 2

    # Momentum
    if 30 < rsi < 70:
        score += 1
    else:
        score -= 1

    # Fib zone
    if price <= fib_618 or price >= fib_382:
        score += 2

    # Direction
    if score >= 3 and trend_up:
        return symbol, "BUY", price, price*1.01, price*0.995, score

    if score <= -3 and not trend_up:
        return symbol, "SELL", price, price*0.99, price*1.005, score

    return None

# -------------------------
# SCAN ALL MARKETS
# -------------------------
symbols = ["BTCUSD", "EURUSD", "XAUUSD"]

best_trade = None

for s in symbols:
    price = get_price(s)
    if price:
        result = analyze(s, price)

        if result:
            if not best_trade or result[5] > best_trade[5]:
                best_trade = result

# -------------------------
# SEND BEST SIGNAL ONLY
# -------------------------
if best_trade:
    symbol, direction, entry, tp, sl, score = best_trade

    send(f"""
📊 V5 MARKET SCANNER SIGNAL

Asset: {symbol}
Direction: {direction}

Entry: {round(entry,2)}
TP: {round(tp,2)}
SL: {round(sl,2)}

Strength Score: {score}

Mode: Multi-Market Scanner
""")

else:
    send("📊 V5: No strong setup across all markets")
