from flask import Flask, render_template, request
import requests
import simplejson
import pandas as pd
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import json_item,components, file_html
import json
from datetime import datetime

app = Flask(__name__)

colormap = {'opening': 'red', 'closing': 'green', 'adj_opening': 'blue','adj_closing':'grey'}

@app.route('/',methods=['GET','POST'])
def index():
  df=pd.DataFrame()
  if request.method=='GET':
    return render_template('index_tatar.html')
  else:
    ticker=request.form.get('ticker')
    url='https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?ticker='+ticker+'&api_key=Rbqd6XdpKwEqHn67V-HN' #this is a json file with encoding utf-8.
    json_content = requests.get(url).json()
    dates=[json_content['datatable']['data'][i][1] for i in range(len(json_content['datatable']['data']))]
    df['Dates']=dates
    if request.form.get('feature_close'):
      df['closing']=[json_content['datatable']['data'][i][5] for i in range(len(json_content['datatable']['data']))]
    if request.form.get('feature_open'):
      df['opening']=[json_content['datatable']['data'][i][2] for i in range(len(json_content['datatable']['data']))]
    if request.form.get('feature_adj_close'):
      df['adj_closing']=[json_content['datatable']['data'][i][12] for i in range(len(json_content['datatable']['data']))]
    if request.form.get('feature_adj_open'):
      df['adj_opening']=[json_content['datatable']['data'][i][9] for i in range(len(json_content['datatable']['data']))]
    date_obj=pd.to_datetime(df['Dates'])
    df.set_index(date_obj,inplace=True)
    df.drop('Dates',axis=1,inplace=True)
    frame=df.loc[df.index>datetime(2017,1,1,0,0,0)]
    p = figure(title = "Price Plot", x_axis_type='datetime')
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Price'
    for col in frame.columns:
      p.line(list(frame.index), frame[col], color=colormap[col],legend=col)
    p.legend.location='top_left'
    html=file_html(p,CDN,'price')
    return html

		

if __name__ == '__main__':
  app.run(debug=True)