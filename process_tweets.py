import json
import time
from datetime import datetime
from datetime import timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import cryptocompare
import requests


def calc_bitcoin_price(timestamp):
    url = 'https://min-api.cryptocompare.com/data/histominute?fsym=BTC&tsym=USD&limit=1&e=CCCAGG&toTs=' + timestamp
    response = requests.get(url)
    result = json.loads(response.text)
    close_price_variation = result["Data"][0]['close'] - result["Data"][1]['close']
    high_price_variation = result["Data"][0]['high'] - result["Data"][1]['high']
    low_price_variation = result["Data"][0]['low'] - result["Data"][1]['low']
    open_price_variation = result["Data"][0]['open'] - result["Data"][1]['open']
    volumeFrom_variation = result["Data"][0]['volumefrom'] - result["Data"][1]['volumefrom']
    volumeTo_variation = result["Data"][0]['volumeto'] - result["Data"][1]['volumeto']
    tweets_date.write("close_price_variation = " + str("%.2f" % close_price_variation) + ", "
     + "high_price_variation = " +  str("%.2f" % high_price_variation) +  ", "
     + "low_price_variation = " + str("%.2f" % low_price_variation)  +  ", "
     + "open_price_variation = " + str("%.2f" % open_price_variation) +  ", "
     + "volumeFrom_variation = " + str("%.2f" % volumeFrom_variation) + ", "
     + "volumeTo_variation = " + str("%.2f" % volumeTo_variation) + ", " )

def calc_sentiment(texts):
    neg = 0
    neu = 0
    pos = 0
    for sentence in texts:
        vs = analyzer.polarity_scores(sentence)
        neg += vs['neg']
        neu += vs['neu']
        pos += vs['pos']

    tweets_date.write("neg = " + str("%.2f" % neg) + ", " + "neu = " +  str("%.2f" % neu) +  ", " +  "pos = " + str("%.2f" % pos)  +  "\n" )

def order_by_minute(tweets):
    list_15 = []
    list_16 = []
    list_17 = []
    list_18 = []
    list_19 = []
    list_20 = []
    list_21 = []
    list_22 = []
    list_23 = []
    list_24 = []
    list_25 = []
    list_26 = []
    list_27 = []
    list_28 = []
    list_29 = []
    list_30 = []
    all_tweets = []
    for tweet in tweets:
        t0 = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet["created_at"],'%a %b %d %H:%M:%S +0000 %Y'))
        t0_date_time = datetime.strptime(t0, '%Y-%m-%d %H:%M:%S')

        if(t0_date_time.minute == 15):
            list_15.append(tweet)
        elif t0_date_time.minute == 16:
            list_16.append(tweet);
        elif t0_date_time.minute == 17:
            list_17.append(tweet);
        elif t0_date_time.minute == 18:
            list_18.append(tweet);
        elif t0_date_time.minute == 19:
            list_19.append(tweet);
        elif t0_date_time.minute == 20:
            list_20.append(tweet);
        elif t0_date_time.minute == 21:
            list_21.append(tweet);
        elif t0_date_time.minute == 22:
            list_22.append(tweet);
        elif t0_date_time.minute == 23:
            list_23.append(tweet);
        elif t0_date_time.minute == 24:
            list_24.append(tweet);
        elif t0_date_time.minute == 25:
            list_25.append(tweet);
        elif t0_date_time.minute == 26:
            list_26.append(tweet);
        elif t0_date_time.minute == 27:
            list_27.append(tweet);
        elif t0_date_time.minute == 28:
            list_28.append(tweet);
        elif t0_date_time.minute == 29:
            list_29.append(tweet);
        elif t0_date_time.minute == 30:
            list_30.append(tweet);
        else:
            print("Not Found")

    all_tweets.extend((list_15, list_16, list_17, list_18, list_19, list_20, list_21, list_22, list_23, list_24, list_25, list_26, list_27, list_28, list_29, list_30))
    return all_tweets;


# ================================ Main program ================================

tweets = []
all_tweets = []
tweets_date = open('tweets_date.txt', 'w')
analyzer = SentimentIntensityAnalyzer()

for line in open('bitcoin.json', 'r'):
    tweets.append(json.loads(line))

all_tweets = order_by_minute(tweets)

for tweets in all_tweets:
    tweets_count = len(tweets)
    t0 = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweets[tweets_count-1]["created_at"],'%a %b %d %H:%M:%S +0000 %Y'))
    t0_date_time = datetime.strptime(t0, '%Y-%m-%d %H:%M:%S')
    t1_date_time = t0_date_time + timedelta(seconds=60)ss
    tweets_date.write("t = " + t0 + ", ")
    tweets_date.write("t1 = " + str(t1_date_time) + ", ")
    tweets_date.write("tweets_count = " + str(tweets_count) + ", ")
    calc_bitcoin_price(str('%.0f' % t1_date_time.timestamp()))
    texts = []
    for tweet in tweets:
        texts.append(tweet["text"])
    calc_sentiment(texts)
