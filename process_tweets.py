import json
import time
from datetime import datetime
from datetime import timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import cryptocompare
import requests

# Função que lê arquivo com tweets e retorna um dicionário de minutos X tweets


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

# função que recebe o conjunto de textos de cada minuto e calcula o sentimento
# daquele minuto


def calc_sentiment(texts):
    neg = 0
    neu = 0
    pos = 0
    for sentence in texts:
        vs = analyzer.polarity_scores(sentence)
        neg += vs['neg']
        neu += vs['neu']
        pos += vs['pos']
    if(neg > pos):
        tweets_date.write("false" + "\n")
    elif(pos > neg):
        tweets_date.write("true" + "\n")
    else:
        tweets_date.write("true" + "\n")

# Função que recebe o tempo de cada tweet e calcula o percentual de variação
# do preço de fechamento, maior e menor preço, volume transacionado em btc e
# em $


def calc_bitcoin_price(timestamp):
    url = 'https://min-api.cryptocompare.com/data/histominute?fsym=BTC&tsym=USD&limit=1&e=CCCAGG&toTs=' + timestamp
    response = requests.get(url)
    result = json.loads(response.text)
    close_price_variation = (result["Data"][1]['close'] - result["Data"][0]
                             ['close'])/result["Data"][1]['close']
    close_price_variation *= 100
    price_variation = (result["Data"][1]['high'] - result["Data"][0]
                             ['low'])/result["Data"][1]['low']
    price_variation *= 100
    # high_price_variation = (result["Data"][0]['high'] -
    # result["Data"][0]['high'])/result["Data"][0]['close']
    # high_price_variation *= 100
    # low_price_variation = (result["Data"][0]['low'] -
    # result["Data"][0]['low'])/result["Data"][0]['close']
    # low_price_variation *= 100
    # open_price_variation = (result["Data"][0]['open'] -
    # result["Data"][0]['open'])/result["Data"][0]['close']
    # open_price_variation *= 100
    # volumeTo_variation = (result["Data"][0]['volumeto'] -
    # result["Data"][0]['volumeto'])/result["Data"][0]['close']
    # volumeTo_variation *= 100

    volumeFrom_variation = (result["Data"][1]['volumefrom'] - result["Data"][0]
                            ['volumefrom'])/result["Data"][1]['close']
    volumeFrom_variation *= 100

    if(close_price_variation > 0):
        close_price_up = "true"
    elif(close_price_variation < 0):
        close_price_up = "false"
    else:
        close_price_up = "false"
    # Verifica se o valor calculado corresponde ao tempo lido
    # t0_api = datetime.fromtimestamp(int(result["Data"][0]["time"]))
    # t1_api = datetime.fromtimestamp(int(result["Data"][1]["time"]))
    # tweets_date.write(str(t0_api) + ", " + str(t1_api) + "\n")
    tweets_date.write(close_price_up + ", " +
                      str("%.4f" % close_price_variation) + ", "
                      + str("%.4f" % price_variation) + ", "
                      + str("%.4f" % volumeFrom_variation) + ", ")


tweets_date = open('test_data/13.csv', 'a')
analyzer = SentimentIntensityAnalyzer()
list_dict = get_ordered_dict()
for key in list_dict:
    t0 = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(
        list_dict[key][0]["created_at"], '%a %b %d %H:%M:%S +0000 %Y'))

    t1 = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(
        list_dict[key][-1]["created_at"], '%a %b %d %H:%M:%S +0000 %Y'))

    t0_date_time = datetime.strptime(t0, '%Y-%m-%d %H:%M:%S')
    t1_date_time = t0_date_time + timedelta(seconds=60)
    tweets_date.write(t0 + ", " + t1 + ", ")
    calc_bitcoin_price(str('%.0f' % t1_date_time.timestamp()))
    texts = []
    for tweet in list_dict[key]:
        texts.append(tweet["text"])
    calc_sentiment(texts)
