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
    csv.write("t0,t1,t1_normalized,tweets_count,pos,neg,neu,indicator\n")
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

        t0_date_time = datetime.strptime(t0, '%Y-%m-%d %H:%M:%S')

        t1_normalized = t0_date_time + timedelta(hours=1)

        tweets_count = len(list_dict[key])
        texts = []
        for tweet in list_dict[key]:
            texts.append(tweet["text"])

        scores = calc_sentiment(texts, analyzer)
        indicator = scores[0] / tweets_count
        csv.write(t0 + ", " + t1 + ", " + str(t1_normalized) + ", " + str(tweets_count) + ", " + str(scores[1]) + ", " + str(scores[2]) + ", " + str(scores[3]) + ", " + str('%.3f' % indicator) + "\n")
        last_tweet_timestamp = (t1_normalized - timedelta(hours=3)).timestamp()
    csv.close()
    return last_tweet_timestamp


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


def build_graphs(timestamp):
    print(timestamp)
    # Building Candlestick Graph
    plotly.tools.set_credentials_file(username='Nicacioneto', api_key='7K1twHAOzbFqTaYOwUU0')
    url = "https://min-api.cryptocompare.com/data/histohour?fsym=BTC&tsym=USD&limit=263&toTs=" + str(timestamp)
    response = requests.get(url)
    result = json.loads(response.text)['Data']
    for r in result:
        r['time'] = datetime.utcfromtimestamp(r['time']).strftime('%Y-%m-%d %H:%M:%S')
    df = pd.DataFrame(result)
    trace1 = go.Candlestick(x=df.time,
                            open=df.open,
                            high=df.high,
                            low=df.low,
                            close=df.close, xaxis='x')

    # data = [trace1]
    # fig = go.Figure(data=data, layout=layout)
    # py.iplot(fig, filename='simple_candlestick')

    #Building Sentiment Graph
    df = pd.read_csv(sys.argv[1])
    trace2 = go.Bar(x=df.t1_normalized, y=df.indicator, xaxis='x', yaxis='y2', marker=dict(
        color=make_color(df.indicator), colorscale='Viridis', colorbar = dict(
            title = 'Sentimento',
            titleside = 'top',
        )),)

    layout = go.Layout(
        title = "Candlestick X SentimentGraph",
        xaxis=dict(rangeslider=dict(visible=False), domain=[0, 1]),
        yaxis=dict(domain=[0.5, 1]),
        yaxis2=dict(domain=[0, 0.45], anchor='x')
    )

    # fig = go.Figure(data=data, layout=layout)
    # data = [trace2]
    # py.iplot(fig, filename='sentiment_indicator')

    data = [trace1, trace2]
    fig = go.Figure(data=data, layout=layout)
    # plotly.offline.plot(fig, filename=sys.argv[1][0:15]+ ".html", auto_open=True)
    py.iplot(fig, filename=sys.argv[1][0:15])

def make_color(indicator_data):
    color = []
    for i in indicator_data:
        color.append(float(i))
    return color

def main():
    write_csv_header()
    filenames = [sys.argv[2], sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6],sys.argv[7],sys.argv[8],sys.argv[9],sys.argv[10],sys.argv[11],sys.argv[12],sys.argv[13],sys.argv[14],sys.argv[15],sys.argv[16],sys.argv[17],sys.argv[18],sys.argv[19],sys.argv[20],sys.argv[21],sys.argv[22],sys.argv[23],sys.argv[24],sys.argv[25],sys.argv[26]]
    last_tweet_timestamp = ""
    for name in filenames:
        list_dict = get_ordered_dict(name)
        last_tweet_timestamp = write_csv_body(list_dict)
        list_dict = []
    # build_graphs(last_tweet_timestamp)


if __name__ == '__main__':
    main()
