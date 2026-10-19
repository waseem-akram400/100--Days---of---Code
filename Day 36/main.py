import os
import requests
from dotenv import load_dotenv
from twilio.rest import Client
load_dotenv()
STOCK = "IBM"
COMPANY_NAME = "IBM"
STOCK_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "")
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
def get_stock_movement():
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCK,
        "apikey": STOCK_API_KEY,
    }
    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()
    data = response.json()
    daily_data = data.get("Time Series (Daily)")
    if not daily_data:
        print("Stock data unavailable:", data)
        return None
    dates = sorted(daily_data.keys(), reverse=True)
    if len(dates) < 2:
        print("Not enough daily prices to compare.")
        return None
    latest = float(daily_data[dates[0]]["4. close"])
    previous = float(daily_data[dates[1]]["4. close"])
    change_percent = ((latest - previous) / previous) * 100
    print(f"Latest available date: {dates[0]}")
    print(f"Latest close: ${latest:.2f}")
    print(f"Previous close: ${previous:.2f}")
    print(f"Change: {change_percent:.2f}%")
    return change_percent
def get_news():
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": COMPANY_NAME,
        "sortBy": "publishedAt",
        "pageSize": 3,
        "language": "en",
        "apiKey": NEWS_API_KEY,
    }
    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()
    data = response.json()
    if data.get("status") != "ok":
        print("News service error:", data)
        return []
    articles = data.get("articles", [])
    return articles[:3]
def send_sms(message_text):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID", "")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN", "")
    from_number = os.getenv("TWILIO_PHONE_NUMBER", "")
    to_number = os.getenv("MY_PHONE_NUMBER", "")
    if not all([account_sid, auth_token, from_number, to_number]):
        print("SMS not sent: complete the Twilio details in .env first.")
        print("Message that would have been sent:")
        print(message_text)
        return
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message_text,
        from_=from_number,
        to=to_number,
    )
    print("SMS request submitted. Message SID:", message.sid)
def main():
    if not STOCK_API_KEY or not NEWS_API_KEY:
        print("Please add the stock and news API keys to the .env file.")
        return
    change = get_stock_movement()
    if change is None:
        return
    if abs(change) < 5:
        print("Price movement is below 5%. No alert needed.")
        return
    direction = "??" if change > 0 else "??"
    articles = get_news()
    if not articles:
        send_sms(f"{direction} {COMPANY_NAME} moved {change:.2f}%. No news articles found.")
        return
    for article in articles:
        title = article.get("title") or "No title"
        source = (article.get("source") or {}).get("name", "Unknown source")
        message = (
            f"{direction} {COMPANY_NAME} moved {change:.2f}%.\n"
            f"Headline: {title}\n"
            f"Source: {source}\n"
            f"{article.get('url', '')}"
        )
        send_sms(message)
if __name__ == "__main__":
    main()
