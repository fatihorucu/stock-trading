import requests as rq
from twilio.rest import Client
used_func = bool
STOCK = "TSLA"
COMPANY_NAME = "Tesla"
rate = int

# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
alphavantage_api_key = "# You can get it from alphavantage"
alphavantage_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": alphavantage_api_key
}

response = rq.get(url="https://www.alphavantage.co/query", params=alphavantage_parameters)
response.raise_for_status()
data = response.json()
days_list = [item for item in data["Time Series (Daily)"]]
yesterday = data["Time Series (Daily)"][days_list[0]]
the_day_before = data["Time Series (Daily)"][days_list[1]]
print(yesterday)
print(the_day_before)

def increase_5(yesterday: float, the_day_before: float) -> bool:
    if yesterday > the_day_before and (yesterday - the_day_before) / the_day_before > 0.0001:
        global used_func, rate
        rate = (yesterday - the_day_before) / the_day_before
        used_func = True
        return True


def decrease_5(yesterday: float, the_day_before: float) -> bool:
    if the_day_before > yesterday and (the_day_before - yesterday) / the_day_before > 0.0001:
        global used_func, rate
        rate = (the_day_before - yesterday) / the_day_before
        used_func = False
        return True


# STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.


if decrease_5(float(yesterday["4. close"]), float(the_day_before["4. close"])) \
        or increase_5(float(yesterday["4. close"])
        , float(the_day_before["4. close"])):
    news_apikey = "You can get it from newsapi.org"
    news_parameters = {
        "q": COMPANY_NAME,
        "apiKey": news_apikey,
    }
    r2 = rq.get(url="https://newsapi.org/v2/top-headlines", params=news_parameters)
    r2.raise_for_status()
    news_data = r2.json()
    if news_data["totalResults"] != 0 and news_data["totalResults"] <= 3:
        articles_list = [news_data["articles"]]
    elif news_data["totalResults"] > 3:
        for x in range(3):
            articles_list = [news_data["articles"][x]]
    else:
        raise Exception("No articles found.")

# STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.
    twilio_id = "# You can get it from twilio"
    twilio_token = "# You can get it from twilio"
    client = Client(twilio_id, twilio_token)
    if used_func:
        for item in articles_list:
            message = client.messages.create(
                body=f"{COMPANY_NAME} 🔺{rate}\nHeadline:{item[0]['title']}\nBrief:{item[0]['description']}",
                to="+905060264009",
                from_="+13854328617"
            )
            print(message.status)
    elif not used_func:
        for item in articles_list:
            message = client.messages.create(
                body=f"{COMPANY_NAME} 🔻{rate}\nHeadline:{item[0]['title']}\nBrief:{item[0]['description']}",
                to="+905060264009",
                from_="+13854328617"
            )
            print(message.status)


