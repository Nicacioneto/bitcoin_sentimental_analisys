import json
import time
from datetime import datetime
from datetime import timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import cryptocompare
import requests
import operator
import pdb

def get_ordered_dict():
    list_dict = {}
    for line in open('stream_sources/2018-09-08.json', 'r'):
        try:
            tweet = json.loads(line)
            t = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet[ "created_at"],'%a %b %d %H:%M:%S +0000 %Y'))
            t_date_time = datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
            if t_date_time.minute in list_dict:
                list_dict[t_date_time.minute].append(tweet)
            else:
                list_dict[t_date_time.minute] =  []
                list_dict[t_date_time.minute].append(tweet)
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print('Decoding JSON has failed')
    return list_dict

def calc_sentiment(texts, tweets_count):
    neg = 0
    neu = 0
    pos = 0
    for sentence in texts:
        vs = analyzer.polarity_scores(sentence)
        neg += vs['neg']
        neu += vs['neu']
        pos += vs['pos']

    if(neg > pos):
        tweets_date.write("false" + "\n" )
    elif(pos > neg):
        tweets_date.write("true" +  "\n" )
    else:
        tweets_date.write("true" +  "\n" )

def calc_bitcoin_price(timestamp):
    url = 'https://min-api.cryptocompare.com/data/histominute?fsym=BTC&tsym=USD&limit=1&e=CCCAGG&toTs=' + timestamp
    response = requests.get(url)
    result = json.loads(response.text)
    close_price_variation = (result["Data"][1]['close'] - result["Data"][0]['close'])/result["Data"][1]['close']
    close_price_variation *= 100
    price_variation = (result["Data"][1]['high'] - result["Data"][0]['low'])/result["Data"][1]['low']
    price_variation *= 100
    # high_price_variation = (result["Data"][1]['high'] - result["Data"][0]['high'])/result["Data"][1]['close']
    # high_price_variation *= 100
    # low_price_variation = (result["Data"][1]['low'] - result["Data"][0]['low'])/result["Data"][1]['close']
    # low_price_variation *= 100
    # open_price_variation = (result["Data"][1]['open'] - result["Data"][0]['open'])/result["Data"][1]['close']
    # open_price_variation *= 100
    volumeFrom_variation = (result["Data"][1]['volumefrom'] - result["Data"][0]['volumefrom'])/result["Data"][1]['close']
    volumeFrom_variation *= 100
    # volumeTo_variation = (result["Data"][1]['volumeto'] - result["Data"][0]['volumeto'])/result["Data"][0]['close']
    # volumeTo_variation *= 100

    if(close_price_variation > 0):
        close_price_up = "true"
    elif(close_price_variation < 0):
        close_price_up = "false"
    else:
        close_price_up = "false"

    tweets_date.write(close_price_up + ", " + str("%.4f" % close_price_variation) + ", " +  str("%.4f" % price_variation) + ", " + str("%.4f" % volumeFrom_variation) + ", ")



tweets_date = open('results/2018-10-03.csv', 'a')
analyzer = SentimentIntensityAnalyzer()
list_dict = get_ordered_dict()


for key in sorted(list_dict):
    tweets_count = len(list_dict[key])
    t0 = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(list_dict[key][-1]["created_at"],'%a %b %d %H:%M:%S +0000 %Y'))
    t0_date_time = datetime.strptime(t0, '%Y-%m-%d %H:%M:%S')
    t1_date_time = t0_date_time + timedelta(seconds=60)
    tweets_date.write(t0 + ", ")
    tweets_date.write(str(t1_date_time) + ", ")
    calc_bitcoin_price(str('%.0f' % t1_date_time.timestamp()))
    texts = []
    for tweet in list_dict[key]:
        texts.append(tweet["text"])
    calc_sentiment(texts, tweets_count)
