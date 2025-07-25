import time
import datetime
from keep_alive import keep_alive
from utils import fetch_filings, send_discord_alert, find_news, is_stock_live

CREDIBLE_INVESTORS = [
    "Renaissance Technologies",
    "Carl Icahn",
    "BlackRock",
    "Vanguard Group",
    "ARK Investment Management",
    "Pershing Square Capital Management"
]

EXCHANGES = ["NASDAQ", "NYSE", "AMEX"]
seen = set()

keep_alive()

while True:
    now = datetime.datetime.now(datetime.timezone.utc)
    if now.weekday() >= 5 or now.hour < 13 or now.hour >= 20:
        print("Outside market hours. Sleeping...")
        time.sleep(60 * 15)
        continue

    filings = fetch_filings()
    for filing in filings:
        key = (filing['ticker'], filing['investor'], filing['type'])
        if key in seen:
            continue
        if (
            filing['investor'] in CREDIBLE_INVESTORS and 
            filing['exchange'] in EXCHANGES and 
            is_stock_live(filing['ticker'])
        ):
            news_url = find_news(filing['ticker'])
            send_discord_alert(filing, news_url)
            seen.add(key)

    time.sleep(60 * 15)

from discord_alert import send_discord_alert

test_filing = {
    'ticker': 'TEST',
    'investor': 'Warren Buffett',
    'type': '13F',
    'url': 'https://www.sec.gov/Archives/edgar/data/0000000000/0000000000-00-000000-index.htm',
    'exchange': 'NASDAQ',
    'date': '2025-07-15'
}
send_discord_alert(test_filing, news_url="https://finance.yahoo.com/news/example-news")

