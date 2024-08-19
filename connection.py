import mysql.connector

dbconfig = {
    'host': HOST,
    'user': USER,
    'password': PASSWORD,
    'database': DATABASE,
}

def connect_to_db(dbconfig):
    return mysql.connector.connect(**dbconfig)
