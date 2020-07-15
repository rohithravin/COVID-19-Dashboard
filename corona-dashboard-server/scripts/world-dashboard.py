import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import mysql.connector
import os
from mysql.connector import errorcode
import pandas as pd
import plotly.offline as pyo
import sys
sys.path.insert(1, '../corona-dashboard-server/scripts')
import config
import json
import chart_studio.plotly as py
import chart_studio.tools as tls
import chart_studio

PLOTLY_USERNAME = 'corona_dashboard'
PLOTLY_API_KEY = 'O2OxLYXntLMqm2Ll0AtO'

plotTimeLine = {
    501: 14,
    502: 30,
    503: 90,
    504: None
}


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
#       TOP COUNTRIES STATS     #
#
# ----------------------------- #
worldStats = {
    2100: 'new_cases',
    2200: 'new_cases',
    2500: 'new_deaths',
    2600: 'new_deaths',
    2300: 'total_cases',
    2400: 'total_deaths'
}

def updateWorldStats(traceId, limit_num):
    cnx = openConnection()
    trace = worldStats[traceId]
    time_diff = 0
    if traceId in [2100,2500]:
        time_diff = 1
    sql_stm = "SELECT date , location, {}  FROM corona.world_data WHERE date = curdate() - {} AND location != 'World' ORDER BY {} DESC LIMIT {}".format(trace, time_diff, trace, limit_num) 
    df_stats = pd.read_sql(sql_stm, con = cnx)
    countries = list(df_stats['location'].unique())
    sql_stm_total = ''
    df_total = None
    description = ''
    if traceId in [2100,2200]:
        sql_stm_total = "SELECT location, total_cases as total FROM corona.world_data WHERE date = curdate() AND location IN ({})".format("'" + '\',\''.join(countries) + "'")
        df_total = pd.read_sql(sql_stm_total, con = cnx)
        description = '% Based On Total {}'.format(trace[trace.index('_')+1:].capitalize())
    elif traceId in [2500,2600]:
        sql_stm_total = "SELECT location, total_deaths as total FROM corona.world_data WHERE date = curdate() AND location IN ({})".format("'" + '\',\''.join(countries) + "'")
        df_total = pd.read_sql(sql_stm_total, con = cnx)
        description = '% Based On Total {}'.format(trace[trace.index('_')+1:].capitalize())
    elif traceId in [2300,2400]:
        sql_stm_total = "SELECT location, population as total FROM corona.world_location WHERE location IN ({})".format("'" + '\',\''.join(countries) + "'")
        df_total = pd.read_sql(sql_stm_total, con = cnx)
        description = '% Based On Total Population'
    top_countries_data = {}
    for index, row in df_stats.iterrows():
        top_countries_data[row['location']] = {
            'country': row['location'],
            'total':row[trace],
            'description':description ,
            'percentage': round((( row[trace] / int(df_total.loc[df_total['location'] == row['location']]['total']))* 100) , 2) }
    print(json.dumps({'Top Countries Data': top_countries_data}))

worlTotalPlotInfo = {
                    1100: 'new_cases',
                    1200: 'new_deaths',
                    1300: 'total_cases',
                    1400: 'total_deaths',
                    }
# ----------------------------- #
#
#       UPDATE WORLD PLOT       #
#
# ----------------------------- #

def updateTotalPlot(traceId, timelineId):
    trace = worlTotalPlotInfo[traceId]
    timeline = plotTimeLine[timelineId]
    cnx = openConnection()
    sql_stm = "SELECT date , {}  FROM corona.world_data  WHERE location = 'World' ORDER BY date desc".format(trace)
    df = pd.read_sql(sql_stm, con = cnx)
    df_sub = df.sort_values(by='date', ascending=False)
    if timeline != None:
            df_sub = df_sub.head(timeline)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_sub['date'], y=df_sub[trace], mode='lines+markers', name=trace, fill='tozeroy'))
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="# of People",
        margin=dict(
            l=50,
            r=50,
            b=0,
            t=0,
            pad=4
        ),
        showlegend=False
    )
    closeConnection(cnx)
    chart_studio.tools.set_credentials_file(username=PLOTLY_USERNAME, api_key=PLOTLY_API_KEY)
    fig_url = py.plot(fig, filename='totalWorldPlot', auto_open=False)
    html = tls.get_embed(fig_url)
    final_html_link = html[html.index('https'):html.index('embed')+5] + '?showlink=false&modebar=false&autosize=true'
    print(json.dumps({'Plot Link': final_html_link}))



# ----------------------------- #
#
#       MAIN METHOD BELOW       #
#
# ----------------------------- #
if len(sys.argv) < 2:
        print("Please include method flag.", file=sys.stderr)
        exit(1)
elif sys.argv[1] == '--updateWorldPlot':
    if len(sys.argv) < 4:
        print("Invalid argument list. python cali-dashboard.py [method-flag] [traceId] [timelineId]", file=sys.stderr)
        exit(1)
    try:
        traceId = int(sys.argv[2])
        timelineId = int(sys.argv[3])
    except Exception as err:
        print("Argument not a number.", file=sys.stderr)
        exit(2)
    if traceId not in [1100,1200,1300,1400]:
        print("kindId argument not a valid id.", file=sys.stderr)
        exit(5)
    if timelineId not in [501,502,503,504]:
        print("traceId argument not a valid id.", file=sys.stderr)
        exit(6)
    updateTotalPlot(traceId, timelineId)
elif sys.argv[1] == '--updateTopCountriesData':
    if len(sys.argv) < 4:
        print("Invalid argument list. python cali-dashboard.py [method-flag] [traceId] [numLimit]", file=sys.stderr)
        exit(1)
    try:
        traceId = int(sys.argv[2])
        numLimit = int(sys.argv[3])
    except Exception as err:
        print("Argument not a number.", file=sys.stderr)
        exit(2)
    if traceId not in [2100,2200,2300,2400,2500,2600]:
        print("traceId argument not a valid id.", file=sys.stderr)
        exit(5)
    updateWorldStats(traceId, numLimit)