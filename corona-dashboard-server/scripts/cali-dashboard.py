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
#   GET Total CASES/DEATH PLOT  #
#
# ----------------------------- #
totalKindPlotInfo = {
                'kind':{601: ['total_cases', 'totalcountconfirmed'], 602: ['total_deaths','totalcountdeaths']}, 
                'trace': {401:'county' , 402: 'state', 403: 'bay_area' ,404: 'socal' , 405:'nocal_socal' ,406: 'bay_area_socal', 407:'high_populous'}
               }
def updateTotalPlot(kindId, traceId, county):
    BAR_WIDTH = 0.5
    cnx = openConnection()
    kind_type = totalKindPlotInfo['kind'][kindId]
    kind_trace = totalKindPlotInfo['trace'][traceId]
    fig = go.Figure()
    if kind_trace == 'nocal_socal':
        sql_stm_socal = "SELECT SUM({}) as {} FROM corona.cali_cases WHERE county IN ({}) GROUP BY date ORDER BY date Desc LIMIT 1".format(kind_type[1],kind_type[1],"'" + '\',\''.join(config.SOCAL_COUNTIES) + "'" )
        sql_stm_norcal = "SELECT SUM({}) as {} FROM corona.cali_cases WHERE county IN ({}) GROUP BY date ORDER BY date Desc LIMIT 1".format(kind_type[1],kind_type[1],"'" + '\',\''.join(config.NORCAL_COUNTIES) + "'" )
        total_num_socal = int(pd.read_sql(sql_stm_socal, con = cnx)[kind_type[1]])
        total_num_norcal = int(pd.read_sql(sql_stm_norcal, con = cnx)[kind_type[1]])
        fig.add_trace(go.Bar(
            x=['SOCAL'],
            y=[total_num_socal],
            width=[BAR_WIDTH]
        ))
        fig.add_trace(go.Bar(
            x=['NORCAL'],
            y=[total_num_norcal],
            width=[BAR_WIDTH]
        ))
    elif kind_trace == 'bay_area_socal':
        sql_stm_socal = "SELECT SUM({}) as {} FROM corona.cali_cases WHERE county IN ({}) GROUP BY date ORDER BY date Desc LIMIT 1".format(kind_type[1],kind_type[1],"'" + '\',\''.join(config.SOCAL_COUNTIES) + "'" )
        sql_stm_bayarea = "SELECT SUM({}) as {} FROM corona.cali_cases WHERE county IN ({}) GROUP BY date ORDER BY date Desc LIMIT 1".format(kind_type[1],kind_type[1],"'" + '\',\''.join(config.BAY_AREA_COUNTIES) + "'" )
        total_num_socal = int(pd.read_sql(sql_stm_socal, con = cnx)[kind_type[1]])
        total_num_bayarea = int(pd.read_sql(sql_stm_bayarea, con = cnx)[kind_type[1]])
        fig.add_trace(go.Bar(
            x=['SOCAL'],
            y=[total_num_socal],
            width=[BAR_WIDTH]
        ))
        fig.add_trace(go.Bar(
            x=['Bay Area'],
            y=[total_num_bayarea],
            width=[BAR_WIDTH]
        ))
    elif kind_trace == 'county':
        sql_stm = "SELECT {} FROM corona.cali_cases WHERE county = '{}' ORDER BY date DESC LIMIT 1".format(kind_type[1],county)
        total_num = int(pd.read_sql(sql_stm, con = cnx)[kind_type[1]])
        fig.add_trace(go.Bar(
            x=[county],
            y=[total_num],
            width=[BAR_WIDTH]
        ))
    elif kind_trace == 'state':
        sql_stm = "SELECT date, sum({}) as {} FROM corona.cali_cases GROUP BY date ORDER BY date DESC LIMIT 1".format(kind_type[1],kind_type[1])
        total_num = int(pd.read_sql(sql_stm, con = cnx)[kind_type[1]])
        fig.add_trace(go.Bar(
            x=['California'],
            y=[total_num],
            width=[BAR_WIDTH]
        ))
    elif kind_trace == 'bay_area':
        sql_stm = "SELECT county, {} FROM corona.cali_cases WHERE county IN ({}) AND date = (SELECT date FROM corona.cali_cases ORDER BY date DESC LIMIT 1)".format(kind_type[1],"'" + '\',\''.join(config.BAY_AREA_COUNTIES) + "'" )
        df = pd.read_sql(sql_stm, con = cnx)
        for index, row in df.iterrows():
            fig.add_trace(go.Bar(
                x=[row['county']],
                y=[row[kind_type[1]]],
                width=[BAR_WIDTH]
            ))
    elif kind_trace == 'high_populous':
        sql_stm = "SELECT county, {} FROM corona.cali_cases WHERE county IN ({}) AND date = (SELECT date FROM corona.cali_cases ORDER BY date DESC LIMIT 1)".format(kind_type[1],"'" + '\',\''.join(config.HIGH_POPULOUS_COUNTIES) + "'" )
        df = pd.read_sql(sql_stm, con = cnx)
        for index, row in df.iterrows():
            fig.add_trace(go.Bar(
                x=[row['county']],
                y=[row[kind_type[1]]],
                width=[BAR_WIDTH]
            ))
    elif kind_trace == 'socal':
        sql_stm = "SELECT county, {} FROM corona.cali_cases WHERE county IN ({}) AND date = (SELECT date FROM corona.cali_cases ORDER BY date DESC LIMIT 1)".format(kind_type[1],"'" + '\',\''.join(config.SOCAL_COUNTIES) + "'" )
        df = pd.read_sql(sql_stm, con = cnx)
        for index, row in df.iterrows():
            fig.add_trace(go.Bar(
                x=[row['county']],
                y=[row[kind_type[1]]],
                width=[BAR_WIDTH]
            ))
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
    closeConnection(cnx)
    chart_studio.tools.set_credentials_file(username=PLOTLY_USERNAME, api_key=PLOTLY_API_KEY)
    fig_url = py.plot(fig,  auto_open=False)
    html = tls.get_embed(fig_url)
    final_html_link = html[html.index('https'):html.index('embed')+5] + '?showlink=false&modebar=false&autosize=true'
    print(json.dumps({'Plot Link': final_html_link}))
        

# ----------------------------- #
#
#         GET MIXED PLOTS       #
#
# ----------------------------- #
mixedPlotInfo = {
                'kind':{701: ['age_group', 'cali_cases_age'],
                        702: ['sex','cali_cases_sex'],
                        703: ['race_ethnicity', 'cali_cases_race'] }, 
                
                'trace': {801:['total_cases',{701: 'totalpositive', 702: 'totalpositive2', 703:'cases'}],
                          802: ['total_deaths',{701: 'deaths', 702: 'deaths', 703:'deaths'}],
                          803: ['death_percentage',{701: 'deaths_percentage', 702: 'deaths_percent', 703:'death_percentage'}],
                          804: ['case_percentage',{701: 'case_percent', 702: 'case_percent', 703:'case_percentage'}] }
               }

def updateGroupsKindPlot(kindId,traceId,timelineId):
    cnx = openConnection()
    plotKind = mixedPlotInfo['kind'][kindId]
    plotTrace = mixedPlotInfo['trace'][traceId]
    timeline = plotTimeLine[timelineId]
    fig = go.Figure()
    sql_stm = "SELECT {}, date, {} FROM {}".format(plotKind[0],plotTrace[1][kindId],plotKind[1])
    df = pd.read_sql(sql_stm, con = cnx)
    if plotKind[1] == 'cali_cases_age':
        df = df.replace(to_replace ="65 and Older", value ="65+")  
        df = df.replace(to_replace ="Missing", value ="Unknown")  
    elif plotKind[1] == 'cali_cases_race':
        df = df.replace(to_replace ="Native Hawaiian and other Pacific Islander", value ="Native Hawaiian or Pacific Islander")  
        df = df.replace(to_replace ="Multi-Race", value ="Multiracial")  
    for group in list(df[plotKind[0]].unique()):
        df_sub = df.loc[df[plotKind[0]] == group].sort_values(by='date', ascending=False)            
        if timeline != None:
            df_sub = df_sub.head(timeline)
        fig.add_trace(go.Scatter(x=df_sub['date'], y=df_sub[plotTrace[1][kindId]], mode='lines+markers', name=group))
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
    fig_url = py.plot(fig, auto_open=False)
    html = tls.get_embed(fig_url)
    final_html_link = html[html.index('https'):html.index('embed')+5] + '?showlink=false&modebar=false&autosize=true'
    print(json.dumps({'Plot Link': final_html_link}))


# ----------------------------- #
#
#    GET NEW CASES/DEATH PLOT   #
#
# ----------------------------- #
newKindPlotInfo = {
                'kind':{301: ['new_cases', 'newcountconfirmed'], 302: ['new_deaths','newcountdeaths']}, 
                'trace': {401:'county' , 402: 'state', 403: 'bay_area' ,404: 'socal' , 405:'nocal_socal' ,406: 'bay_area_socal', 407:'high_populous'}
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
         xaxis_title="Date",
        yaxis_title="# of People",
        margin=dict(
            l=50,
            r=50,
            b=0,
            t=0,
            pad=4
        )
    )
    closeConnection(cnx)
    chart_studio.tools.set_credentials_file(username=PLOTLY_USERNAME, api_key=PLOTLY_API_KEY)
    fig_url = py.plot(fig, auto_open=False)
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
elif sys.argv[1] == '--updateMixedPlots':
    if len(sys.argv) < 5:
        print("Invalid argument list. python cali-dashboard.py [method-flag] [kindId] [traceId] [timelineId]", file=sys.stderr)
        exit(1)
    try:
        kindId = int(sys.argv[2])
        traceId = int(sys.argv[3])
        timelineId = int(sys.argv[4])
    except Exception as err:
        print("Argument not a number.", file=sys.stderr)
        exit(2)
    if kindId not in [701,702, 703]:
        print("kindId argument not a valid id.", file=sys.stderr)
        exit(5)
    if traceId not in [801,802,803,804]:
        print("traceId argument not a valid id.", file=sys.stderr)
        exit(6)
    if timelineId not in [501,502,503,504]:
        print("traceId argument not a valid id.", file=sys.stderr)
        exit(6)
    updateGroupsKindPlot(kindId,traceId,timelineId)
elif sys.argv[1] == '--updateTotalPlot':
    if len(sys.argv) < 5:
        print("Invalid argument list. python cali-dashboard.py [method-flag] [kindId] [traceId] [county]", file=sys.stderr)
        exit(1)
    try:
        kindId = int(sys.argv[2])
        traceId = int(sys.argv[3])
    except Exception as err:
        print("Argument not a number.", file=sys.stderr)
        exit(2)
    county_input = ' '.join(list(sys.argv)[4:])
    if county_input not in config.ALL_COUNTIES:
        print("County argument not a county.", file=sys.stderr)
        exit(3)
    if kindId not in [601,602]:
        print("kindId argument not a valid id.", file=sys.stderr)
        exit(5)
    if traceId not in [401,402,403,404,405,406,407]:
        print("traceId argument not a valid id.", file=sys.stderr)
        exit(6)
    updateTotalPlot(kindId, traceId, county_input)
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
    newKindPlot(kindId,traceId,timelineId,county_input)
else:
    print("Invalid flag argument. python cali-dashboard.py [method-flag]", file=sys.stderr)
    exit(2)