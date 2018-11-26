import json
import time
from datetime import datetime
from datetime import timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import requests
import sys
import os

def write_csv_header():
    csv = open(os.environ['HOME'] + '/Desktop/bitcoin_sentimental_analisys/' + sys.argv[1], 'a')
    csv.write("t0,t1,tweets_count,pos,neg,neu,indicator\n")
    csv.close()

def write_csv_body(list_dict):
    last_tweet_timestamp = ""
    analyzer = SentimentIntensityAnalyzer()
    csv = open(os.environ['HOME'] + '/Desktop/bitcoin_sentimental_analisys/' + sys.argv[1], 'a')
    for key in list_dict:
        t0 = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(
            list_dict[key][0]["created_at"], '%a %b %d %H:%M:%S +0000 %Y'))

        t1 = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(
            list_dict[key][-1]["created_at"], '%a %b %d %H:%M:%S +0000 %Y'))

        tweets_count = len(list_dict[key])
        texts = []
        for tweet in list_dict[key]:
            texts.append(tweet["text"])

        scores = calc_sentiment(texts, analyzer)
        indicator = scores[0] / tweets_count
        csv.write(t0 + ", " + t1 + ", " + str(tweets_count) + ", " + str(scores[1]) + ", " + str(scores[2]) + ", " + str(scores[3]) + ", " + str('%.3f' % indicator) + "\n")
        # last_tweet_timestamp = (t1_normalized - timedelta(hours=3)).timestamp()
    csv.close()
    return 0

def get_ordered_dict(filename):
    list_dict = {}
    for line in open(os.environ['HOME'] + '/Documents/outubro/' + filename, 'r'):
        try:
            tweet = json.loads(line)
            t = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(
                tweet["created_at"], '%a %b %d %H:%M:%S +0000 %Y'))
            t = t[0:10]
            if t in list_dict:
                list_dict[t].append(tweet)
            else:
                list_dict[t] = []
                list_dict[t].append(tweet)
            print('Decoding JSON has success')
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print('Decoding JSON has failed')
    return list_dict

def calc_sentiment(texts, analyzer):
    scores = []
    total_score = 0
    pos = 0
    neg = 0
    neu = 0
    for text in texts:
        compound_score = analyzer.polarity_scores(text)
        total_score += compound_score['compound']
        if(compound_score['compound'] >= 0.05):
            pos +=1
        elif(compound_score['compound'] > -0.05 and compound_score['compound'] < 0.05):
            neu += 1
        else:
            neg += 1

    scores.extend((total_score, pos, neg, neu))
    return scores


def main():
    write_csv_header()
    filenames = [sys.argv[2], sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6],
                 sys.argv[7],sys.argv[8],sys.argv[9],sys.argv[10],sys.argv[11],
                 sys.argv[12],sys.argv[13],sys.argv[14],sys.argv[15],sys.argv[16],
                 sys.argv[17],sys.argv[18],sys.argv[19],sys.argv[20],sys.argv[21],
                 sys.argv[22],sys.argv[23],sys.argv[24],sys.argv[25],sys.argv[26],
                 sys.argv[27],sys.argv[28],sys.argv[29],sys.argv[30],sys.argv[31],
                 sys.argv[32],sys.argv[33],sys.argv[34],sys.argv[35],sys.argv[36],
                 sys.argv[37],sys.argv[38],sys.argv[39]]
    last_tweet_timestamp = ""
    for name in filenames:
        list_dict = get_ordered_dict(name)
        last_tweet_timestamp = write_csv_body(list_dict)
        list_dict = []

if __name__ == '__main__':
    main()
