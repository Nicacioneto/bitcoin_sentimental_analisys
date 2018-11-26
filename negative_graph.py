import json
from datetime import datetime
import pandas as pd
import requests
import plotly
import plotly.plotly as py
from plotly.graph_objs import *

url = "https://min-api.cryptocompare.com/data/histohour?fsym=BTC&tsym=USD&limit=361&toTs=" + str(1542326400)
response = requests.get(url)
result = json.loads(response.text)['Data']
for r in result:
    r['time'] = datetime.utcfromtimestamp(r['time']).strftime('%Y-%m-%d %H:%M:%S')

df0 = pd.DataFrame(result)
df1 = pd.read_csv("01_15_dataframe.csv")

trace1 = {
  "x": df0.time.tolist(),
  "y": df0.close.tolist(),
  "legendgroup": 1,
  "mode": "lines",
  "name": "Bitcoin",
  "type": "scatter",
  "xsrc": "Nicacioneto:27:f7ff6d",
  "ysrc": "Nicacioneto:27:72a5e6"
}

trace2 = {
  "x": df0.time.tolist(),
  "y": df1.neg.tolist(),
  "fill": "tozeroy",
  "fillcolor": "rgba(255, 77, 14, 0.2)",
  "line": {"color": "rgb(255, 77, 14)"},
  "mode": "lines",
  "name": "Tweets Negativos",
  "type": "scatter",
  "xsrc": "Nicacioneto:27:f7ff6d",
  "yaxis": "y2",
  "ysrc": "Nicacioneto:27:bbc8f4"
}
data = Data([trace1, trace2])
layout = {
  "autosize": True,
  "legend": {
    "x": -0.0972490923174,
    "y": 1.22233417667
  },
  "title": "Bitcoin Vs Tweets Negativos",
  "xaxis": {
    "autorange": True,
    "range": ["2018-11-01 01:00", "2018-11-16"],
    "title": "<br>",
    "type": "date"
  },
  "yaxis": {
    "autorange": True,
    "range": [5233.33333333, 6626.66666667],
    "title": "Preço",
    "type": "linear"
  },
  "yaxis2": {
    "autorange": True,
    "overlaying": "y",
    "range": [0, 3032.63157895],
    "side": "right",
    "title": "QUantidade",
    "type": "linear"
  }
}
fig = Figure(data=data, layout=layout)
plotly.offline.plot(fig, "test.html", auto_open=True)
