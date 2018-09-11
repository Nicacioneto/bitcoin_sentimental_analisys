import json
import time
from datetime import datetime
from datetime import timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import cryptocompare
import requests

def get_ordered_dict():
    tweets = []
    for line in open('bitcoin.json', 'r'):
        tweets.append(json.loads(line))
        list_dict = {}
    for tweet in tweets:
        t = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet["created_at"],'%a %b %d %H:%M:%S +0000 %Y'))
        t_date_time = datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
        if t_date_time.minute in list_dict:
            list_dict[t_date_time.minute].append(tweet)
        else:
            list_dict[t_date_time.minute] =  []
            list_dict[t_date_time.minute].append(tweet)
    return list_dict

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

tweets_date = open('tweets_date.txt', 'w')
analyzer = SentimentIntensityAnalyzer()
list_dict = get_ordered_dict()
for key in sorted(list_dict):
        tweets_count = len(list_dict[key])
        t0 = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(list_dict[key][-1]["created_at"],'%a %b %d %H:%M:%S +0000 %Y'))
        t0_date_time = datetime.strptime(t0, '%Y-%m-%d %H:%M:%S')
        t1_date_time = t0_date_time + timedelta(seconds=60)
        tweets_date.write("t = " + t0 + ", ")
        tweets_date.write("t1 = " + str(t1_date_time) + ", ")
        tweets_date.write("tweets_count = " + str(tweets_count) + ", ")
        calc_bitcoin_price(str('%.0f' % t1_date_time.timestamp()))
        texts = []
        for tweet in list_dict[key]:
            texts.append(tweet["text"])
        calc_sentiment(texts)
