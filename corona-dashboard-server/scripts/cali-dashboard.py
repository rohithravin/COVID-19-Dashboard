import mysql.connector
import os
from mysql.connector import errorcode
import pandas as pd
import config
import sys
import json

def openConnection():
    cnx = mysql.connector.connect(user = config.MYSQL_USERNAME, password = config.MYSQL_PASSWORD,
                                    host = config.MYSQL_HOST, allow_local_infile=True,
                                    database = config.MYSQL_DB )
    cursor = cnx.cursor()
    return cnx,cursor

def closeConnection(cnx,cursor):
    cursor.close()
    cnx.close()

def getDailyData(county):
    cnx,cursor = openConnection()

    # get daily testing data
    try:
        sql_stm = 'SELECT * FROM corona.cali_testing ORDER BY date desc LIMIT 2'
        cursor.execute(sql_stm)
    except mysql.connector.Error as err:
            print(err.msg, file=sys.stderr)
    tested_nums = []
    for (date, tested) in cursor:
        tested_nums.append(tested)
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

    closeConnection(cnx,cursor)

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
else:
    print("Invalid flag argument. python cali-dashboard.py [method-flag]", file=sys.stderr)
    exit(2)