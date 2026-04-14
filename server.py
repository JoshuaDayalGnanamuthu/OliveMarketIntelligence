from flask import Flask, jsonify, render_template
import flask
from dotenv import load_dotenv
import finnhub
import os
from datetime import date, timedelta
import time

load_dotenv("./.env")

app = Flask(__name__)
client = finnhub.Client(api_key=os.getenv("API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/news/<ticker>")
def get_company_news(ticker="AAPL"):
    today = date.today()
    three_days_ago = today - timedelta(days=3)
    news = client.company_news(ticker, _from=three_days_ago.isoformat(), to=today.isoformat())
    return jsonify(news)

@app.route("/quote/<ticker>")
def get_stock_quote(ticker="AAPL"):
    quote = client.quote(ticker)
    return jsonify(quote)

@app.route("/crypto/<symbol>")
def get_crypto_quote(symbol="BINANCE:BTCUSDT"):
    now = int(time.time())
    one_min_ago = now - 60
    data = client.crypto_candles(symbol, "1", one_min_ago, now)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
