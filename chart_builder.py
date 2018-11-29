import psycopg2
import datetime
from datetime import timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests
import json
import plotly
import plotly.plotly as py
from plotly.graph_objs import *


def get_last_hour_tweets():
    conn = psycopg2.connect("dbname=testdb user=nicacio")
    cur = conn.cursor()
    final_date = datetime.datetime.utcnow()
    initial_date = datetime.datetime.utcnow() - timedelta(hours=1)
    cur.execute("select * from tweets WHERE date >= %s and date <= %s", (initial_date,final_date))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def calc_last_hour_sentiment(texts):
    analyzer = SentimentIntensityAnalyzer()
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

def get_last_hour_financial_data(final_date):
    final_date = int(final_date.timestamp())
    url = "https://min-api.cryptocompare.com/data/histohour?fsym=BTC&tsym=USD&limit=1&toTs=" + str(final_date)
    response = requests.get(url)
    financial_data = json.loads(response.text)['Data']
    for r in financial_data:
        r['time'] = datetime.datetime.utcfromtimestamp(r['time']).strftime('%Y-%m-%d %H:%M:%S')
    return financial_data

# def build_sentimental_candlestick_graph(financial_data, indicador):
#     plotly.tools.set_credentials_file(username='Nicacioneto', api_key='7K1twHAOzbFqTaYOwUU0')
#     candlestick_data = Candlestick(x=[financial_data[-1]["time"]],
#                                         open=[financial_data[-1]["open"]],
#                                         high=[financial_data[-1]["high"]],
#                                         low=[financial_data[-1]["low"]],
#                                         close=[financial_data[-1]["close"]])
    # sentiment_data = Bar(x=[financial_data[-1]["time"]], y=[indicador], marker=dict(
    #     color=float(indicador), colorscale='Viridis', colorbar = dict(
    #         x= 1.03,
    #         y= 0.35,
    #         len= 0.75,
    #         thickness= 30,
    #         title= 'Sentimento',
    #         titleside = 'top',
    #         xpad= 10,
    #         ypad= 10,
    #     )),)

    # data = [candlestick_data, sentiment_data]
    # plot_url = py.plot(data, filename='candlestick_sentimental_grid', fileopt='extend')

def update_positive_sentimental_graph(financial_data, positive):
    trace1 = {
      "x": [ [financial_data[-1]["time"]] ],
      "y": [ [financial_data[-1]["close"]] ],
      "type": "scatter"
    }

    trace2 = {
      "x": [ [financial_data[-1]["time"]] ],
      "y": [positive],
      "type": "scatter"
    }
    data = Data([trace1, trace2])
    plot_url = py.plot(data, filename='btc_positivos', fileopt='extend')


def update_negative_sentimental_graph(financial_data, negative):
    trace1 = {
      "x": [ [financial_data[-1]["time"]] ],
      "y": [ [financial_data[-1]["close"]] ],
      "type": "scatter"
    }

    trace2 = {
      "x": [ [financial_data[-1]["time"]] ],
      "y": [negative],
      "type": "scatter"
    }
    data = Data([trace1, trace2])
    plot_url = py.plot(data, filename='btc_negativos', fileopt='extend')


def main():
    rows = get_last_hour_tweets()
    texts = []
    for row in rows:
        texts.append(row[1])
    scores = calc_last_hour_sentiment(texts)
    indicador = scores[0] / len(texts)
    indicador = round(indicador, 3)
    final_date = rows[-1][2]
    financial_data = get_last_hour_financial_data(final_date)
    #update_sentimental_candlestick_graph(financial_data, indicador)
    update_positive_sentimental_graph(financial_data, scores[1])
    update_negative_sentimental_graph(financial_data, scores[2])

if __name__ == '__main__':
    main()


# initial_date = rows[0][2]
# final_date = rows[-1][2]
# limit = final_date - initial_date
# limit = int(round(((limit.total_seconds()/60)/60),0))
# for i in range(limit):
#     initial_date +=
