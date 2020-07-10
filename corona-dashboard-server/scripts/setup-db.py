import mysql.connector
from dotenv import load_dotenv
import os
from mysql.connector import errorcode
import csv
import pandas as pd

# Load environment variables from `.env` file.
load_dotenv('../.env')

cnx = mysql.connector.connect(user = os.environ.get("MYSQL_USERNAME"),
                                password = os.environ.get("MYSQL_PASSWORD"),
                                host = os.environ.get("MYSQL_HOST"),
                                allow_local_infile=True)
cursor = cnx.cursor()

TABLES = {}

TABLES['zipcode'] = (
    "CREATE TABLE `zipcode` ("
    "  `zipcode` INT NOT NULL,"
    "  `primary_city` VARCHAR(250) NOT NULL,"
    "  `state` VARCHAR(5) NOT NULL,"
    "  `county` VARCHAR(250) NOT NULL"
    ") ENGINE=InnoDB")



def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(os.environ.get("MYSQL_DB")))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(os.environ.get("MYSQL_DB")))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(os.environ.get("MYSQL_DB")))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(os.environ.get("MYSQL_DB")))
        cnx.database = os.environ.get("MYSQL_DB")
    else:
        print(err)
        exit(1)

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            sql_stm = "TRUNCATE TABLE {}".format(table_name)
            cursor.execute(sql_stm)
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

zipcode_df = pd.read_csv('../data/zipcode.csv') 
zipcode_df = zipcode_df.loc[zipcode_df['state'] == 'CA'][['zip','primary_city','state','county']]
zipcode_data = [tuple(x) for x in zipcode_df.values.tolist()]

# print(zipcode_data[0:5])
print("Loading zipcode data:", end="")
try:
    cursor.executemany(
    """ 
        INSERT INTO zipcode
        (
            zipcode,
            primary_city,
            state,
            county
        )
        VALUE (%s, %s, %s, %s)
    """, zipcode_data )
except mysql.connector.Error as err:
    print(err.msg)
else:
    print("OK")
cnx.commit()
    



cursor.close()
cnx.close()