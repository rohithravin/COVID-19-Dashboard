import warnings
warnings.filterwarnings("ignore")
import plotly.graph_objects as go
import pandas as pd
import mysql.connector
import pandas as pd
import sys
sys.path.insert(1, '../corona-dashboard-server/scripts')
import config
import json
import chart_studio.plotly as py
import chart_studio.tools as tls
import numpy as np
import chart_studio
import matplotlib.pyplot as plt
from scipy import optimize
import itertools
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, acf, pacf,arma_order_select_ic
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima_model import ARIMA
from datetime import datetime

PLOTLY_USERNAME = config.PLOTLY_USERNAME
PLOTLY_API_KEY = config.PLOTLY_API_KEY

# ----------------------------- #
#
#     OPEN MYSQL CONNECTION     #
#
# ----------------------------- #
def openConnection():
    cnx = mysql.connector.connect(user = config.MYSQL_USERNAME, password = config.MYSQL_PASSWORD,
                                    host = config.MYSQL_HOST, allow_local_infile=True,
                                    database = config.MYSQL_DB )
    return cnx


# ----------------------------- #
#
#     CLOSE MYSQL CONNECTION    #
#
# ----------------------------- #
def closeConnection(cnx):
    cnx.close()


# ----------------------------- #
#
#        VALIDATE COUNTRY       #
#
# ----------------------------- #
def validateCountry(country):
    cnx = openConnection()
    sql_stm = 'SELECT DISTINCT(location) FROM corona.world_data'
    df = pd.read_sql(sql_stm, con = cnx)
    countries = list(df['location'])
    country = country.strip().lower()
    if country not in [x.lower() for x in countries]:
        print(json.dumps({'message': 'country doesn\'t exist.', 'python_code':501}))
    else:
        print(json.dumps({'message': 'country exists.', 'python_code':100, 'country':country.strip().lower().title()}))

# ----------------------------- #
#
#       LOGISTIC MODELING       #
#
# ----------------------------- #
def logistic_forecast(column_name, country,dual_display):

    def logistic_model(x,a,b,c):
        return c/(1+np.exp(-(x-b)/a))

    cnx = openConnection()
    sql_stm = 'SELECT date, {} FROM corona.world_data WHERE location = "{}" ORDER BY date ASC'.format(column_name,country)
    df = pd.read_sql(sql_stm, con = cnx)
    df['timestep'] = range(0,len(df))
    x = list(df.iloc[:,2])
    y = list(df.iloc[:,1])
    fit = optimize.curve_fit(logistic_model,x,y,p0=[2,100,150000])
    sol = int(optimize.fsolve(lambda x : logistic_model(x,fit[0][0],fit[0][1],fit[0][2]) - int(fit[0][2]),fit[0][1]))
    errors = [np.sqrt(fit[1][i][i]) for i in [0,1,2]]
    expected_low = fit[0][2] - errors[2]
    expected_high = fit[0][2] + errors[2]
    threshold_date = (df['date'][0] + pd.DateOffset(days=sol)).strftime("%B %d, %Y")
    pred_x = list(range(max(x),sol))
    date_range = pd.date_range(start=df['date'][0], periods=sol)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['date'], y=df[column_name], mode='lines+markers',line = dict(width=3)))
    fig.add_trace(go.Scatter(x=date_range, y=[logistic_model(i,fit[0][0],fit[0][1],fit[0][2]) for i in x+pred_x], mode='lines',line = dict(width=2)))
    fig.update_layout(
        margin=dict(
            l=50,
            r=50,
            b=0,
            t=0,
            pad=4
        ),
        showlegend=False
    )
    if dual_display:
        snapshot_df = df.tail(60)
        snapshot_x = list(snapshot_df.iloc[:,2])
        snapshot_y = list(snapshot_df.iloc[:,1])
        snapshot_pred_x = list(range(max(snapshot_x),max(snapshot_x)+60  ))
        snapshot_date_range = pd.date_range(start=snapshot_df['date'][snapshot_df.index.to_list()[0]], periods=max(snapshot_x)+60)
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=snapshot_df['date'], y=snapshot_df[column_name], mode='lines+markers',line = dict(width=3)))
        fig2.add_trace(go.Scatter(x=snapshot_date_range, y=[logistic_model(i,fit[0][0],fit[0][1],fit[0][2]) for i in snapshot_x+snapshot_pred_x], mode='lines',line = dict(width=2)))
        fig2.update_layout(
            margin=dict(
                l=50,
                r=50,
                b=0,
                t=0,
                pad=4
            ),
            showlegend=False
        )
        return fig, fig2, expected_low, expected_high, threshold_date, format(int(round(fit[0][2])),',')
    return fig,  expected_low, expected_high, threshold_date, format(int(round(fit[0][2])),',')



# ----------------------------- #
#
#        ARIMA MODELING         #
#
# ----------------------------- #
def arima_forecast(column_name,country,dual_display):

    def roll(df,case):
        ts=df[['date',case]]
        ts=ts.set_index('date')
        ts.astype('int64')
        a=len(ts.loc[(ts[column_name]>=10)])
        ts=ts[-a:]
        return (ts.rolling(window=4,center=False).mean().dropna())

    #Arima modeling for ts
    def arima(ts):
        p=d=q=range(0,6)
        a=99999
        pdq=list(itertools.product(p,d,q))

        #Determining the best parameters
        for var in pdq:
            try:
                warnings.filterwarnings("ignore")
                model = ARIMA(ts, order=var, freq='D')
                result = model.fit(disp=0)

                if (result.aic<=a) :
                    a=result.aic
                    param=var
            except:
                continue

        #Modeling
        warnings.filterwarnings("ignore")
        model = ARIMA(ts, order=param, freq='D')
        result = model.fit(disp=0)
        pred=result.forecast(steps=90)

        return pred[0],pred[1],pred[2]


    cnx = openConnection()
    sql_stm = 'SELECT date, {} FROM corona.world_data WHERE location = "{}" ORDER BY date ASC'.format(column_name,country)
    df = pd.read_sql(sql_stm, con = cnx)
    tsC1=roll(df,column_name)
    preds, err,CI =arima(tsC1)

    time_stamps = list(pd.date_range(df['date'].iloc[-1] + pd.DateOffset(1),periods=90))
    pred_list = list(preds)
    lower_ci = list(CI[:, 0])
    upper_ci = list(CI[:, 1])
    nans_list = np.empty(14)
    nans_list[:]  = np.nan
    row_lists = list(zip(time_stamps,pred_list,lower_ci,upper_ci))
    pred_df = pd.DataFrame(row_lists, columns = ['date', 'predictins','lower_ci','upper_ci'])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['date'], y=df[column_name], mode='lines',line = dict(width=3)))
    fig.add_trace(go.Scatter(x=pred_df['date'], y=pred_df['predictins'], mode='lines',line = dict(color='firebrick',width=3) ))
    fig.add_trace(go.Scatter(x=pred_df['date'], y=pred_df['lower_ci'], mode='lines',line = dict(color='grey',width=1)))
    fig.add_trace(go.Scatter(x=pred_df['date'], y=pred_df['upper_ci'], mode='lines',fill='tonexty',line = dict(color='grey',width=1)))
    fig.update_layout(
            margin=dict(
                l=50,
                r=50,
                b=0,
                t=0,
                pad=4
            ),
            showlegend=False
        )
    if dual_display:
        snapshot_df = df.tail(30)
        snapshot_pred_df = pred_df.head(30)
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=snapshot_df['date'], y=snapshot_df[column_name], mode='lines',line = dict(width=3)))
        fig2.add_trace(go.Scatter(x=snapshot_pred_df['date'], y=snapshot_pred_df['predictins'], mode='lines',line = dict(color='firebrick',width=3) ))
        fig2.add_trace(go.Scatter(x=snapshot_pred_df['date'], y=snapshot_pred_df['lower_ci'], mode='lines',line = dict(color='grey',width=1)))
        fig2.add_trace(go.Scatter(x=snapshot_pred_df['date'], y=snapshot_pred_df['upper_ci'], mode='lines',fill='tonexty',line = dict(color='grey',width=1)))
        fig2.update_layout(
                margin=dict(
                    l=50,
                    r=50,
                    b=0,
                    t=0,
                    pad=4
                ),
                showlegend=False
            )
        return fig,fig2
    return fig




# ----------------------------- #
#
#     MAIN FORECAST METHOD      #
#
# ----------------------------- #

forecastLookUp = {
    1234: 'total_cases',
    1235: 'total_deaths',
    1236: 'new_cases',
    1237: 'new_deaths'
}

def getForecasts(traceId,country, dual_display):
    if traceId in [1234,1235]:
        plots  = logistic_forecast(forecastLookUp[traceId], country, dual_display)
    elif traceId in [1236,1237]:
        plots = arima_forecast(forecastLookUp[traceId], country, dual_display)
    chart_studio.tools.set_credentials_file(username=PLOTLY_USERNAME, api_key=PLOTLY_API_KEY)
    if dual_display:
        fig_url = py.plot(plots[0], auto_open=False)
        html = tls.get_embed(fig_url)
        final_html_link = html[html.index('https'):html.index('embed')+5] + '?showlink=false&modebar=false&autosize=true'

        fig_url2 = py.plot(plots[1], auto_open=False)
        html2 = tls.get_embed(fig_url2)
        final_html_link2 = html2[html2.index('https'):html2.index('embed')+5] + '?showlink=false&modebar=false&autosize=true'

        print(json.dumps({'Plot Full Link': final_html_link,
                        'Plot Short Link':final_html_link2,
                        'Expected Low': plots[2],
                        'Expected High': plots[3],
                        'Expected Date': plots[4],
                        'Expected': plots[5]}))

    else:
        fig_url = py.plot(plots[0], filename = 'total_case_death_plot', auto_open=False)
        html = tls.get_embed(fig_url)
        final_html_link = html[html.index('https'):html.index('embed')+5] + '?showlink=false&modebar=false&autosize=true'
        print(json.dumps({'Plot Link': final_html_link,
                        'Expected Low': plots[1],
                        'Expected High': plots[2],
                        'Expected Date': plots[3],
                        'Expected': plots[4]}))


# ----------------------------- #
#
#       MAIN METHOD BELOW       #
#
# ----------------------------- #
if len(sys.argv) < 2:
        print("Please include method flag.", file=sys.stderr)
        exit(1)
elif sys.argv[1] == '--getForcast':
    if len(sys.argv) < 5:
        print("Invalid argument list. python country-forecast.py [method-flag] [traceId] [dual_display] [country] ", file=sys.stderr)
        exit(1)
    try:
        traceId = int(sys.argv[2])
        dual_display = int(sys.argv[3])
    except Exception as err:
        print("Argument not a number.", file=sys.stderr)
        exit(2)
    country_input = ' '.join(list(sys.argv)[4:])
    if traceId not in [1234,1235,1236,1237]:
        print("traceId argument not a valid id.", file=sys.stderr)
        exit(6)
    if dual_display not in [1,0]:
        print("traceId argument not a valid id.", file=sys.stderr)
        exit(6)
    getForecasts(traceId,country_input, dual_display)
elif sys.argv[1] == '--validateCountry':
    if len(sys.argv) < 3:
        print("Invalid argument list. python country-forecast.py [method-flag] [country] ", file=sys.stderr)
        exit(1)
    country_input = ' '.join(list(sys.argv)[2:])
    validateCountry(country_input)
