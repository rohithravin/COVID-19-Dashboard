import mysql.connector
import os
from mysql.connector import errorcode
import pandas as pd
import sys
import config
import json

cnx = mysql.connector.connect(user = config.MYSQL_USERNAME, password = config.MYSQL_PASSWORD,
                                host = config.MYSQL_HOST, allow_local_infile=True,
                                database = config.MYSQL_DB )

cursor = cnx.cursor()

if len(sys.argv) != 2:
    print("Invalid argument list.", file=sys.stderr)
    exit(1)

try:
    zipcode_input = int(sys.argv[1])
except Exception as err:
    print("Argument not a number.", file=sys.stderr)
    exit(2)

sql_stm = "SELECT * FROM zipcode WHERE zipcode = {}".format(zipcode_input)

try:
    cursor.execute(sql_stm)
except mysql.connector.Error as err:
        print(err.msg, file=sys.stderr)

err_flag = True

for (zipcode, primary_city, state,county) in cursor:
    if county.strip() in config.NORCAL_COUNTIES:
        print(json.dumps({'county':county, 'zipcode':zipcode, 'caliSection':'NORCAL'}))
        err_flag = False
    else:
        print(json.dumps({'county':county, 'zipcode':zipcode, 'caliSection':'SOCAL'}))
        err_flag = False
if err_flag:
    print('Zipcode doesn\'t exist.',file=sys.stderr)