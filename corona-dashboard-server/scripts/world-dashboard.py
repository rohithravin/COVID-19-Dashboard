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

PLOTLY_USERNAME = config.PLOTLY_USERNAME
PLOTLY_API_KEY = config.PLOTLY_API_KEY

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
#         COUNTRY PLOT          #
#
# ----------------------------- #

countryPlot = {
    9100: 'new_cases', # today
    9200: 'new_deaths', # today
    9300: 'total_cases',
    9400: 'total_deaths'
}

def getCountryPlot(country, traceId, timelineId, output_type):
    cnx = openConnection()
    trace = countryPlot[traceId]
    timeline = plotTimeLine[timelineId]
    sql_stm = 'SELECT date, {} FROM corona.world_data WHERE location = "{}" ORDER BY date DESC'.format(trace,country)
    df = pd.read_sql(sql_stm, con = cnx)
    if timeline != None:
        df = df.head(timeline)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['date'], y=df[trace], mode='lines+markers'))
    fig.update_layout(
        margin=dict(
            l=50,
            r=50,
            b=0,
            t=0,
            pad=4
        )
    )
    chart_studio.tools.set_credentials_file(username=PLOTLY_USERNAME, api_key=PLOTLY_API_KEY)
    fig_url = py.plot(fig,  auto_open=False)
    html = tls.get_embed(fig_url)
    final_html_link = html[html.index('https'):html.index('embed')+5] + '?showlink=false&modebar=false&autosize=true'
    if output_type == 'return':
        return final_html_link
    elif output_type == 'print':
        print(json.dumps({'Plot Link': final_html_link}))

# ----------------------------- #
#
#          COUNTRY DATA         #
#
# ----------------------------- #
def getCountryData(country,traceId,timelineId):
    cnx = openConnection()
    sql_stm = 'SELECT DISTINCT(location) FROM corona.world_data'
    df = pd.read_sql(sql_stm, con = cnx)
    countries = list(df['location'])
    country = country.strip().lower()
    if country not in [x.lower() for x in countries]:
        print(json.dumps({'message': 'country doesn\'t exist.', 'python_code':501}))
    else:
        country = country.title()
        # New Cases
        sql_stm = "SELECT date,new_cases FROM corona.world_data WHERE location = '{}' AND date != CURDATE() ORDER BY date DESC LIMIT 2".format(country)
        df = pd.read_sql(sql_stm, con = cnx)
        new_cases = list(df['new_cases'])
        new_cases_data = {}
        new_cases_data['data'] = new_cases[0]
        new_cases_data['data_percentage'] = round((( abs(new_cases[0] - new_cases[1]) /  new_cases[1] ) * 100),2)
        if new_cases[0] >= new_cases[1]:
            new_cases_data['direction'] = 'increase'
        else:
            new_cases_data['direction'] = 'decrease'
        new_cases_data['title'] = 'New Cases'
        # New Deaths
        sql_stm = "SELECT date,location,new_deaths FROM corona.world_data WHERE location = '{}' AND date != CURDATE() ORDER BY date DESC LIMIT 2".format(country)
        df = pd.read_sql(sql_stm, con = cnx)
        new_deaths = list(df['new_deaths'])
        new_deaths_data = {}
        new_deaths_data['data'] = new_deaths[0]
        new_deaths_data['data_percentage'] = round((( abs(new_deaths[0] - new_deaths[1]) /  new_deaths[1] ) * 100),2)
        if new_deaths[0] >= new_deaths[1]:
            new_deaths_data['direction'] = 'increase'
        else:
            new_deaths_data['direction'] = 'decrease'
        new_deaths_data['title'] = 'New Deaths'
        # Total Cases
        sql_stm = "SELECT date,location,total_cases FROM corona.world_data WHERE location = '{}' AND date != CURDATE() ORDER BY date DESC LIMIT 2".format(country)
        df = pd.read_sql(sql_stm, con = cnx)
        total_cases = list(df['total_cases'])
        total_cases_data = {}
        total_cases_data['data'] = total_cases[0]
        total_cases_data['data_percentage'] = round((( abs(total_cases[0] - total_cases[1]) /  total_cases[1] ) * 100),2)
        if total_cases[0] >= total_cases[1]:
            total_cases_data['direction'] = 'increase'
        else:
            total_cases_data['direction'] = 'decrease'
        total_cases_data['title'] = 'Total Cases'
        # Total Deaths
        sql_stm = "SELECT date,location,total_deaths FROM corona.world_data WHERE location = '{}' AND date != CURDATE() ORDER BY date DESC LIMIT 2".format(country)
        df = pd.read_sql(sql_stm, con = cnx)
        total_deaths = list(df['total_deaths'])
        total_deaths_data = {}
        total_deaths_data['data'] = total_deaths[0]
        total_deaths_data['data_percentage'] = round((( abs(total_deaths[0] - total_deaths[1]) /  total_deaths[1] ) * 100),2)
        if total_deaths[0] >= total_deaths[1]:
            total_deaths_data['direction'] = 'increase'
        else:
            total_deaths_data['direction'] = 'decrease'
        total_deaths_data['title'] = 'Total Deaths'
        country_data = [new_cases_data, new_deaths_data, total_cases_data, total_deaths_data]
        fig_link = getCountryPlot (country, traceId,timelineId,'return')
        print(json.dumps({'country_data': country_data, 'python_code':100, 'country':country, 'plot_link': fig_link }))
    

# ----------------------------- #
#
#       TOP COUNTRIES PLOT      #
#
# ----------------------------- #
worldStatsPlot = {
    7100: 'new_cases', # today
    7200: 'new_deaths', # today
    7300: 'total_cases',
    7400: 'total_deaths'
}

def getTopCountries(traceId, limit):
    cnx = openConnection()
    trace = worldStatsPlot[traceId]
    sql_stm = ("SELECT date,location, {} " 
        "FROM corona.world_data "
        "WHERE location != 'World' AND date = CURDATE()"
        "ORDER BY {} DESC LIMIT {}".format(trace,trace,limit))
    df = pd.read_sql(sql_stm, con = cnx)
    return list(df['location'])

def updateTopCountriesPlot(traceId, timelineId,limit):
    cnx = openConnection()
    trace = worldStatsPlot[traceId]
    timeline = plotTimeLine[timelineId]
    top_countries = getTopCountries(traceId, limit)
    fig = go.Figure()
    sql_stm = "SELECT date, location, {} FROM corona.world_data WHERE location IN ({})".format(trace,"'" + '\',\''.join(top_countries) + "'")
    df = pd.read_sql(sql_stm, con = cnx)
    for country in list(df['location'].unique()):
        df_sub = df.loc[df['location'] == country].sort_values(by='date', ascending=False)            
        if timeline != None:
            df_sub = df_sub.head(timeline)
        fig.add_trace(go.Scatter(x=df_sub['date'], y=df_sub[trace], mode='lines+markers', name=country))
    fig.update_layout(
        margin=dict(
            l=50,
            r=50,
            b=0,
            t=0,
            pad=4
        )
    )
    chart_studio.tools.set_credentials_file(username=PLOTLY_USERNAME, api_key=PLOTLY_API_KEY)
    fig_url = py.plot(fig,  auto_open=False)
    html = tls.get_embed(fig_url)
    final_html_link = html[html.index('https'):html.index('embed')+5] + '?showlink=false&modebar=false&autosize=true'
    print(json.dumps({'Plot Link': final_html_link}))

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
    if traceId in [2200,2600]:
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
    top_countries_data = []
    for index, row in df_stats.iterrows():
        top_countries_data.append( {
            'country': row['location'],
            'total':row[trace],
            'description':description ,
            'percentage': round((( row[trace] / int(df_total.loc[df_total['location'] == row['location']]['total']))* 100) , 2) } )
    output = {}
    output['topCountriesData'] = top_countries_data
    print(json.dumps({'Top Countries Data': output}))

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
    fig_url = py.plot(fig,  auto_open=False)
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
elif sys.argv[1] == '--updateTopCountriesPlot':
    if len(sys.argv) < 5:
        print("Invalid argument list. python cali-dashboard.py [method-flag] [traceId] [timelineId] [numLimit]", file=sys.stderr)
        exit(1)
    try:
        traceId = int(sys.argv[2])
        timelineId = int(sys.argv[3])
        numLimit = int(sys.argv[4])
    except Exception as err:
        print("Argument not a number.", file=sys.stderr)
        exit(2)
    if traceId not in [7100,7200,7300,7400]:
        print("traceId argument not a valid id.", file=sys.stderr)
        exit(5)
    if timelineId not in [501,502,503,504]:
        print("traceId argument not a valid id.", file=sys.stderr)
        exit(6)
    updateTopCountriesPlot(traceId, timelineId, numLimit)
elif sys.argv[1] == '--getCountryData':
    if len(sys.argv) < 4:
        print("Invalid argument list. python cali-dashboard.py [method-flag] [traceId] [timelineId] [country]", file=sys.stderr)
        exit(1)
    try:
        traceId = int(sys.argv[2])
        timelineId = int(sys.argv[3])
    except Exception as err:
        print("Argument not a number.", file=sys.stderr)
        exit(2)
    country_input = ' '.join(list(sys.argv)[4:])
    if traceId not in [9100,9200,9300,9400]:
        print("traceId argument not a valid id.", file=sys.stderr)
        exit(5)
    if timelineId not in [501,502,503,504]:
        print("traceId argument not a valid id.", file=sys.stderr)
        exit(6)
    getCountryData(country_input,traceId,timelineId)
elif sys.argv[1] == '--getCountryPlot':
    if len(sys.argv) < 5:
        print("Invalid argument list. python cali-dashboard.py [method-flag] [traceId] [timelineId] [output_type] [country]", file=sys.stderr)
        exit(1)
    try:
        traceId = int(sys.argv[2])
        timelineId = int(sys.argv[3])
    except Exception as err:
        print("Argument not a number.", file=sys.stderr)
        exit(2)
    country_input = ' '.join(list(sys.argv)[5:])
    if traceId not in [9100,9200,9300,9400]:
        print("traceId argument not a valid id.", file=sys.stderr)
        exit(5)
    if timelineId not in [501,502,503,504]:
        print("traceId argument not a valid id.", file=sys.stderr)
        exit(6)
    getCountryPlot(country_input,traceId,timelineId, 'print')
