import mysql.connector
import os
from mysql.connector import errorcode
import pandas as pd
import config

cnx = mysql.connector.connect(user = config.MYSQL_USERNAME, password = config.MYSQL_PASSWORD,
                                host = config.MYSQL_HOST, allow_local_infile=True,
                                database = config.MYSQL_DB )
cursor = cnx.cursor()

DATA_URLS = {
                'cali_cases_age' : "https://data.ca.gov/dataset/590188d5-8545-4c93-a9a0-e230f0db7290/resource/339d1c4d-77ab-44a2-9b40-745e64e335f2/download/case_demographics_age.csv",
                'cali_cases_sex' : "https://data.ca.gov/dataset/590188d5-8545-4c93-a9a0-e230f0db7290/resource/ee01b266-0a04-4494-973e-93497452e85f/download/case_demographics_sex.csv",
                'cali_cases_race' : "https://data.ca.gov/dataset/590188d5-8545-4c93-a9a0-e230f0db7290/resource/7e477adb-d7ab-4d4b-a198-dc4c6dc634c9/download/case_demographics_ethnicity.csv",
                'cali_cases' : "https://data.ca.gov/dataset/590188d5-8545-4c93-a9a0-e230f0db7290/resource/926fd08f-cc91-4828-af38-bd45de97f8c3/download/statewide_cases.csv",
                'cali_testing' : "https://data.ca.gov/dataset/efd6b822-7312-477c-922b-bccb82025fbe/resource/b6648a0d-ff0a-4111-b80b-febda2ac9e09/download/statewide_testing.csv"
            }

for key in DATA_URLS.keys():
    data = pd.read_csv(DATA_URLS[key]).dropna()
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