import json
import time
from datetime import datetime
from datetime import timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd

def get_ordered_dict():
    list_dict = {}
    for line in open('stream_sources/test_data/2018-10-13-ts.txt', 'r'):
        try:
            tweet = json.loads(line)
            t = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(
                tweet["created_at"], '%a %b %d %H:%M:%S +0000 %Y'))
            t = t[8:16]
            if t in list_dict:
                list_dict[t].append(tweet)
            else:
                list_dict[t] = []
                list_dict[t].append(tweet)
            print('Decoding JSON has success')
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print('Decoding JSON has failed')
    return list_dict


def calc_sentiment(texts):
    open_index = 0
    close_index = -1
    open_sentiment_value = analyzer.polarity_scores(texts[open_index])
    close_sentiment_value = analyzer.polarity_scores(texts[close_index])
    while(open_sentiment_value['pos'] == 0 or close_sentiment_value['pos'] == 0):
        open_index += 1
        close_index -= 1
        open_sentiment_value = analyzer.polarity_scores(texts[open_index])
        close_sentiment_value = analyzer.polarity_scores(texts[close_index])

    dataframe.write(str(open_sentiment_value['pos']) + ", ")
    dataframe.write(str(close_sentiment_value['pos']) + "\n")

    # pos = []
    # neg = []
    # for sentence in texts:
    #     vs = analyzer.polarity_scores(sentence)
    #     pos.append(vs['pos'])
    #     neg.append(vs['neg'])
    #
    # high_sentiment_value = max(pos)
    # low_sentiment_value = max(neg)
    # dataframe.write(str(low_sentiment_value) + ", ")
    # dataframe.write(str(high_sentiment_value) + "\n")


def build_graph():
    plotly.tools.set_credentials_file(username='Nicacioneto', api_key='7K1twHAOzbFqTaYOwUU0')
    df = pd.read_csv("dataframe.csv")
    trace = go.Candlestick(x=df.time,
                           open=df.open,
                           high=df.high,
                           low=df.low,
                           close=df.close)
    layout = go.Layout(
        xaxis=dict(
            rangeslider=dict(
                visible=False
            )
        )
    )
    data = [trace]
    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig, filename='simple_candlestick')


list_dict = get_ordered_dict()
dataframe = open('dataframe.csv', 'a')
analyzer = SentimentIntensityAnalyzer()

for key in list_dict:
    t0 = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(
        list_dict[key][0]["created_at"], '%a %b %d %H:%M:%S +0000 %Y'))

    dataframe.write(t0 + ", ")

    texts = []
    for tweet in list_dict[key]:
        texts.append(tweet["text"])
    calc_sentiment(texts)
