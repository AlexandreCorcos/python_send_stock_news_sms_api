import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "your api key"
NEWS_API_KEY = "your api key"
TWILIO_API_KEY = "your api key"
TWILIO_SID = "your sid"
TWILIO_PHONE_NUMBER = "+44XXXXXXXXX"
TWILIO_PHONE_SEND = "+44XXXXXXXXX"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

news_params = {
    "q": COMPANY_NAME,
    "apikey": NEWS_API_KEY,
}


response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yestarday_data = data_list[0]
yestarday_closing_price = yestarday_data["4. close"]

before_yestarday_data = data_list[1]
before_yestarday_closing_price = before_yestarday_data["4. close"]
print(yestarday_closing_price, before_yestarday_closing_price)

difference = float(yestarday_closing_price) - float(before_yestarday_closing_price)
up_down = None
if difference > 0:
    up_down = "💲🔺"
else:
    up_down = "💲🔻"
print(difference)

diff_percent = round((difference / float(yestarday_closing_price)) * 100)
print(diff_percent)

if abs(diff_percent) > 0:
    print("Get news")
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    three_articles = articles[:3]
    print(three_articles)

    formatted_articles = [f"{STOCK_NAME}: {up_down} {diff_percent}%\nHeadLine: {articles['title']}. \nURL: {articles['url']}" for articles in three_articles]
    print(formatted_articles)

    client = Client(TWILIO_SID, TWILIO_API_KEY)
    for articles in formatted_articles:
        message = client.messages.create(
            body=articles,
            from_=TWILIO_PHONE_NUMBER,
            to=TWILIO_PHONE_SEND,
        )
