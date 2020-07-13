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
#    GET NEW CASES/DEATH PLOT   #
#
# ----------------------------- #
newKindPlotInfo = {
                'kind':{301: ['new_cases', 'newcountconfirmed'], 302: ['new_deaths','newcountdeaths']}, 
                'trace': {401:'county' , 402: 'state', 403: 'bay_area' ,404: 'socal' , 405:'nocal_socal' ,406: 'bay_area_socal', 407:'high_populous'}
               }
plotTimeLine = {
    501: 14,
    502: 30,
    503: 90,
    504: None
}

def newKindPlot(kindId, traceId, timeline, county):
    cnx = openConnection()
    kind_type = newKindPlotInfo['kind'][kindId]
    kind_trace = newKindPlotInfo['trace'][traceId]
    kind_timeline = plotTimeLine[timeline]
    fig = go.Figure()
    if kind_trace == 'bay_area_socal':
        sql_stm_bay_area = 'SELECT date , SUM({}) as {}  FROM corona.cali_cases WHERE county IN ({}) GROUP BY date'.format(kind_type[1],kind_type[1], "'" + '\',\''.join(config.BAY_AREA_COUNTIES) + "'")
        sql_stm_socal = 'SELECT date , SUM({}) as {}  FROM corona.cali_cases WHERE county IN ({}) GROUP BY date'.format(kind_type[1],kind_type[1], "'" + '\',\''.join(config.SOCAL_COUNTIES) + "'")
        df_bay_area = pd.read_sql(sql_stm_bay_area, con = cnx)
        df_socal = pd.read_sql(sql_stm_socal, con = cnx)
        df_bay_area = df_bay_area.sort_values(by='date', ascending=False)
        df_socal = df_socal.sort_values(by='date', ascending=False)
        if kind_timeline != None:
            df_bay_area = df_bay_area.head(kind_timeline)
            df_socal = df_socal.head(kind_timeline)
        fig.add_trace(go.Scatter(x=df_bay_area['date'], y=df_bay_area[kind_type[1]], mode='lines+markers', name='Bay Area'))
        fig.add_trace(go.Scatter(x=df_socal['date'], y=df_socal[kind_type[1]], mode='lines+markers', name='SoCal'))
    elif kind_trace == 'nocal_socal':
        sql_stm_norcal = 'SELECT date , SUM({}) as {}  FROM corona.cali_cases WHERE county IN ({}) GROUP BY date'.format(kind_type[1],kind_type[1], "'" + '\',\''.join(config.NORCAL_COUNTIES) + "'")
        sql_stm_socal = 'SELECT date , SUM({}) as {}  FROM corona.cali_cases WHERE county IN ({}) GROUP BY date'.format(kind_type[1],kind_type[1], "'" + '\',\''.join(config.SOCAL_COUNTIES) + "'")
        df_norcal = pd.read_sql(sql_stm_norcal, con = cnx)
        df_socal = pd.read_sql(sql_stm_socal, con = cnx)
        df_norcal = df_norcal.sort_values(by='date', ascending=False)
        df_socal = df_socal.sort_values(by='date', ascending=False)
        if kind_timeline != None:
            df_norcal = df_norcal.head(kind_timeline)
            df_socal = df_socal.head(kind_timeline)
        fig.add_trace(go.Scatter(x=df_norcal['date'], y=df_norcal[kind_type[1]], mode='lines+markers', name='NorCal'))
        fig.add_trace(go.Scatter(x=df_socal['date'], y=df_socal[kind_type[1]], mode='lines+markers', name='SoCal'))
    elif kind_trace == 'county':
        sql_stm = 'SELECT date , county, {}  FROM corona.cali_cases WHERE county = {}'.format(kind_type[1], "'" + county + "'")
        df = pd.read_sql(sql_stm, con = cnx)
        df_sub = df.sort_values(by='date', ascending=False)
        if kind_timeline != None:
                df_sub = df_sub.head(kind_timeline)
        fig.add_trace(go.Scatter(x=df_sub['date'], y=df_sub[kind_type[1]], mode='lines+markers', name=county))
    elif kind_trace == 'high_populous':
        sql_stm = 'SELECT date , county,{}  FROM corona.cali_cases WHERE county IN ({})'.format(kind_type[1], "'" + '\',\''.join(config.HIGH_POPULOUS_COUNTIES) + "'")
        df = pd.read_sql(sql_stm, con = cnx)
        for county in config.HIGH_POPULOUS_COUNTIES:
            df_sub = df.loc[df['county'] == county].sort_values(by='date', ascending=False)
            if kind_timeline != None:
                df_sub = df_sub.head(kind_timeline)
            fig.add_trace(go.Scatter(x=df_sub['date'], y=df_sub[kind_type[1]], mode='lines+markers', name=county))
    elif kind_trace == 'socal':
        sql_stm = 'SELECT date , county,{}  FROM corona.cali_cases WHERE county IN ({})'.format(kind_type[1], "'" + '\',\''.join(config.SOCAL_COUNTIES) + "'")
        df = pd.read_sql(sql_stm, con = cnx)
        for county in config.SOCAL_COUNTIES:
            df_sub = df.loc[df['county'] == county].sort_values(by='date', ascending=False)
            if kind_timeline != None:
                df_sub = df_sub.head(kind_timeline)
            fig.add_trace(go.Scatter(x=df_sub['date'], y=df_sub[kind_type[1]], mode='lines+markers', name=county))
    elif kind_trace == 'bay_area':
        sql_stm = 'SELECT date , county,{}  FROM corona.cali_cases WHERE county IN ({})'.format(kind_type[1], "'" + '\',\''.join(config.BAY_AREA_COUNTIES) + "'")
        df = pd.read_sql(sql_stm, con = cnx)
        for county in config.BAY_AREA_COUNTIES:
            df_sub = df.loc[df['county'] == county].sort_values(by='date', ascending=False)
            if kind_timeline != None:
                df_sub = df_sub.head(kind_timeline)
            fig.add_trace(go.Scatter(x=df_sub['date'], y=df_sub[kind_type[1]], mode='lines+markers', name=county))
    elif kind_trace == 'state':
        sql_stm = 'SELECT date , SUM({}) as {}  FROM corona.cali_cases GROUP BY date'.format(kind_type[1],kind_type[1])
        df = pd.read_sql(sql_stm, con = cnx)
        df_sub = df.sort_values(by='date', ascending=False)
        if kind_timeline != None:
                df_sub = df_sub.head(kind_timeline)
        fig.add_trace(go.Scatter(x=df_sub['date'], y=df_sub[kind_type[1]], mode='lines+markers', name='California'))
    fig.update_layout(
         xaxis_title="# of People",
        yaxis_title="Date",
        margin=dict(
            l=50,
            r=50,
            b=0,
            t=0,
            pad=4
        )
    )
    closeConnection(cnx)
    username = 'rohithravin' # your username
    api_key = 'OkgmZv3fqjkRl3XGs7Gf' # your api key - go to profile > settings > regenerate key
    chart_studio.tools.set_credentials_file(username=username, api_key=api_key)
    fig_url = py.plot(fig, filename = 'new_case_death_plot', auto_open=False)
    html = tls.get_embed(fig_url)
    final_html_link = html[html.index('https'):html.index('embed')+5] + '?showlink=false&modebar=false&autosize=true'
    print(json.dumps({'Plot Link': final_html_link}))


# ----------------------------- #
#
#       GET DAILY COVID DATA    #
#
# ----------------------------- #
def getDailyData(county):
    cnx = openConnection()
    cursor = cnx.cursor()
    # get daily testing data
    try:
        sql_stm = 'SELECT tested FROM corona.cali_testing ORDER BY date desc LIMIT 2'
        cursor.execute(sql_stm)
    except mysql.connector.Error as err:
            print(err.msg, file=sys.stderr)
    tested_nums = []
    for tested in cursor:
        tested_nums.append(int(tested[0]))
    daily_test_dict = {}
    daily_test_dict['daily_tested'] = abs(tested_nums[0] - tested_nums[1])
    daily_test_dict['daily_test_percentage'] = round(((daily_test_dict['daily_tested']/tested_nums[1]) * 100),2)
    if tested_nums[0] >= tested_nums[1]:
        daily_test_dict['direction'] = 'increase'
    else:
        daily_test_dict['direction'] = 'decrease'
    # get daily cases and deaths (state)
    try:
        sql_stm =  '''
            SELECT 
                SUM(newcountconfirmed), SUM(newcountdeaths)
            FROM corona.cali_cases
            GROUP BY date
            ORDER BY date desc
            LIMIT 2
        '''
        cursor.execute(sql_stm)
    except mysql.connector.Error as err:
            print(err.msg, file=sys.stderr)
    db_data = []
    for (newcountconfirmed, newcountdeaths) in cursor:
        db_data.append([int(newcountconfirmed), int(newcountdeaths)])
    
    daily_case_state = {}
    daily_case_state['newCaseCount'] = db_data[0][0]
    daily_case_state['newCaseCount_percentage'] = round((( abs(db_data[0][0] - db_data[1][0]) /  db_data[1][0] ) * 100),2)
    if db_data[0][0] >= db_data[1][0]:
        daily_case_state['direction'] = 'increase'
    else:
        daily_case_state['direction'] = 'decrease'

    daily_death_state = {}
    daily_death_state['newCaseCount'] = db_data[0][1]
    daily_death_state['newCaseCount_percentage'] = round((( abs(db_data[0][1] - db_data[1][1]) /  db_data[1][1] ) * 100),2)
    if db_data[0][1] >= db_data[1][1]:
        daily_death_state['direction'] = 'increase'
    else:
        daily_death_state['direction'] = 'decrease'

    # get daily cases (county)
    try:
        sql_stm =  '''
            SELECT SUM(newcountconfirmed)
            FROM corona.cali_cases
            WHERE county = '{}'
            GROUP BY date
            ORDER BY date desc
            LIMIT 2
        '''.format(county)
        cursor.execute(sql_stm)
    except mysql.connector.Error as err:
            print(err.msg, file=sys.stderr)
    db_data = []
    for newcountconfirmed in cursor:
        db_data.append(int(newcountconfirmed[0]))
    
    daily_case_county = {}
    daily_case_county['newCaseCount'] = db_data[0]
    daily_case_county['newCaseCount_percentage'] = round((( abs(db_data[0] - db_data[1]) /  db_data[1] ) * 100),2)
    if db_data[0] >= db_data[1]:
        daily_case_county['direction'] = 'increase'
    else:
        daily_case_county['direction'] = 'decrease'

    dailyData = {}
    dailyData['daily_test_state'] = daily_test_dict
    dailyData['daily_case_state'] = daily_case_state
    dailyData['daily_death_state'] = daily_death_state
    dailyData['daily_case_county'] = daily_case_county
    print(json.dumps(dailyData))

    cursor.close()
    closeConnection(cnx)

# ----------------------------- #
#
#       MAIN METHOD BELOW       #
#
# ----------------------------- #
if len(sys.argv) < 2:
        print("Please include method flag.", file=sys.stderr)
        exit(1)
if sys.argv[1] == '--calDailyData':
    if len(sys.argv) < 3:
        print("Invalid argument list. python cali-dashboard.py [method-flag] [county]", file=sys.stderr)
        exit(1)
    county_input = ' '.join(list(sys.argv)[2:])
    if county_input not in config.ALL_COUNTIES:
        print("County argument not a county.", file=sys.stderr)
        exit(3)
    getDailyData(county_input)
elif sys.argv[1] == '--updateNewPlot':
    if len(sys.argv) < 6:
        print("Invalid argument list. python cali-dashboard.py [method-flag] [kindId] [traceId] [timelineId] [county]", file=sys.stderr)
        exit(1)
    try:
        kindId = int(sys.argv[2])
        traceId = int(sys.argv[3])
        timelineId = int(sys.argv[4])
    except Exception as err:
        print("Argument not a number.", file=sys.stderr)
        exit(2)
    county_input = ' '.join(list(sys.argv)[5:])
    if county_input not in config.ALL_COUNTIES:
        print("County argument not a county.", file=sys.stderr)
        exit(3)
    if kindId not in [301,302]:
        print("kindId argument not a valid id.", file=sys.stderr)
        exit(5)
    if traceId not in [401,402,403,404,405,406,407]:
        print("traceId argument not a valid id.", file=sys.stderr)
        exit(6)
    if timelineId not in [501,502,503,504]:
        print("traceId argument not a valid id.", file=sys.stderr)
        exit(6)
    if county_input not in config.ALL_COUNTIES:
        print("County argument not a county.", file=sys.stderr)
        exit(3)
    newKindPlot(kindId,traceId,timelineId,county_input)
else:
    print("Invalid flag argument. python cali-dashboard.py [method-flag]", file=sys.stderr)
    exit(2)