import requests
import os

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def fetch_filings():
    # Example API response mock
    return [
        {
            "ticker": "XYZ",
            "investor": "Renaissance Technologies",
            "type": "13F",
            "exchange": "NASDAQ",
            "url": "https://www.sec.gov/Archives/edgar/data/0000320193/000032019324000010/0000320193-24-000010-index.htm"
        }
    ]

def send_discord_alert(filing, news_url=None):
    if not WEBHOOK_URL:
        print("No webhook URL configured.")
        return

    content = (
        f"🚨 **New Filing Alert!**\n\n"
        f"📈 **Ticker:** {filing['ticker']}\n"
        f"🏦 **Investor:** {filing['investor']}\n"
        f"🗂️ **Filing Type:** {filing['type']}\n"
        f"💼 **Exchange:** {filing['exchange']}\n"
        f"🔗 [View Filing]({filing['url']})\n"
    )

    if news_url:
        content += f"📰 [Related News]({news_url})"

    payload = {"content": content}
    requests.post(WEBHOOK_URL, json=payload)

def find_news(ticker):
    return f"https://www.google.com/search?q={ticker}+stock+news"

def is_stock_live(ticker):
    try:
        response = requests.get(f"https://api.newdata.io/stock-check?ticker={ticker}")
        return response.status_code == 200 and response.json().get("is_live", False)
    except Exception:
        return False