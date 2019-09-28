import sqlite3
from sqlite3 import Error
from sqlalchemy import create_engine
 
def create_connection(database):
    
    e = create_engine(database)

    conn = None
    try:
        conn = e.connect()
        return conn
    except Error as e:
        print(e)
 
    return conn
 
 
def create_table(conn, create_table_sql):

    try:
        conn.execute(create_table_sql)
    except Error as e:
        print(e)
 
 
def main():
 
    sql_create_signals_table = """ CREATE TABLE IF NOT EXISTS signals (
                                        id integer PRIMARY KEY,
                                        latitude float NOT NULL,
                                        longtitude float NOT NULL,
                                        level integer,
                                        date integer,
                                        operator text NOT NULL,
                                        ntype text NOT NULL DEFAULT 'unknown'
                                    ); """
 
    conn = create_connection('sqlite:///db/tnc.db')

    if conn is not None:

        create_table(conn, sql_create_signals_table)

        print("Tables are created")
    else:
        print("Error")
 
 
if __name__ == '__main__':
    main()