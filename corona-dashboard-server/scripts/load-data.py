import mysql.connector
import os
from mysql.connector import errorcode
import pandas as pd
import config

cnx = mysql.connector.connect(user = config.MYSQL_USERNAME, password = config.MYSQL_PASSWORD,
                                host = config.MYSQL_HOST, allow_local_infile=True,
                                database = config.MYSQL_DB )
cursor = cnx.cursor()

for key in config.DATA_URLS.keys():
    data = pd.read_csv(config.DATA_URLS[key])
    if key in ['world_location', 'world_data']:
        data = data.fillna(0)
    else:
        data = data.dropna()

    mysql_data = [tuple(x) for x in data.values.tolist()]

    print("Clearing {} data: ".format(key), end="")
    try:
        sql_stm = "TRUNCATE TABLE {}".format(key)
        cursor.execute(sql_stm)
    except mysql.connector.Error as err:
        print(err.msg)
    else:
        print("OK")
    cnx.commit()

    print("Loading {} data: ".format(key), end="")
    sql_stm = 'INSERT INTO {} ( '.format(key) 
    for x in range(len(data.columns)):
        if x == len(data.columns) - 1:
            sql_stm += str(data.columns[x]) + ' ) '
        else:
            sql_stm += str(data.columns[x]) + ', '
    sql_stm += 'VALUE ('
    for x in range(len(mysql_data[0])):
        if x == len(mysql_data[0]) - 1:
            sql_stm += '%s )'
        else:
            sql_stm += '%s, '
    try:
        cursor.executemany(sql_stm, mysql_data )
    except mysql.connector.Error as err:
        print(err.msg)
    else:
        print("OK")
    cnx.commit()

cursor.close()
cnx.close()