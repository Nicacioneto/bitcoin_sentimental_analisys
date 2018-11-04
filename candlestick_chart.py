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


def get_ordered_dict(filename):
    list_dict = {}
    for line in open('stream_sources/' + filename, 'r'):
        try:
            tweet = json.loads(line)
            t = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(
                tweet["created_at"], '%a %b %d %H:%M:%S +0000 %Y'))
            t = t[8:13]
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
    score = 0
    for text in texts:
        score_pos = analyzer.polarity_scores(text)
        score += score_pos['compound']
    return score


def build_graphs(timestamp):
    # Building Candlestick Graph
    plotly.tools.set_credentials_file(username='Nicacioneto', api_key='7K1twHAOzbFqTaYOwUU0')
    url = "https://min-api.cryptocompare.com/data/histohour?fsym=BTC&tsym=USD&limit=192&toTs=" + timestamp
    response = requests.get(url)
    result = json.loads(response.text)['Data']
    for r in result:
        r['time'] = datetime.utcfromtimestamp(r['time']).strftime('%Y-%m-%d %H:%M:%S')
    df = pd.DataFrame(result)
    trace1 = go.Candlestick(x=df.time,
                            open=df.open,
                            high=df.high,
                            low=df.low,
                            close=df.close)

    # data = [trace1]
    # fig = go.Figure(data=data, layout=layout)
    # py.iplot(fig, filename='simple_candlestick')

    #Building Sentiment Graph
    df = pd.read_csv("dataframe.csv")
    trace2 = go.Bar(x=df.t1_normalized, y=df.indicator, xaxis='x2', yaxis='y2', marker=dict(
        color=make_color(df.indicator), colorscale='Viridis', showscale=True),)

    layout = go.Layout(
        title = "Candlestick X SentimentGraph",
        xaxis=dict(rangeslider=dict(visible=False), domain=[0, 1]),
        yaxis=dict(domain=[0.5, 1]),
        xaxis2=dict(domain=[0, 1]),
        yaxis2=dict(domain=[0, 0.45], anchor='x2')
    )

    # fig = go.Figure(data=data, layout=layout)
    # data = [trace2]
    # py.iplot(fig, filename='sentiment_indicator')

    data = [trace1, trace2]
    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig, filename='01-08-2018-07-08-2018')


def make_color(indicator_data):
    color = []
    for i in indicator_data:
        color.append(float(i))
    return color


def main():
    dataframe = open(sys.argv[1], 'a')
    dataframe.write("'t0','t1','t1_normalized','tweets_count','indicator'")

    filenames = [sys.argv[2], sys.argv[3]]
    analyzer = SentimentIntensityAnalyzer()


    for name in filenames:
        dataframe = open(sys.argv[1], 'a')

        list_dict = get_ordered_dict(name)

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

            score = calc_sentiment(texts, analyzer)
            indicator = score / tweets_count
            dataframe.write(t0 + ", " + t1 + ", " + str(t1_normalized) + ", " + str(tweets_count) + ", " + str('%.3f' % indicator) + "\n")
        list_dict = {}
        dataframe.close()


if __name__ == '__main__':
    main()
