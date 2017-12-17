import psycopg2
import config
import pandas as pd
import csv
from itertools import islice
from sqlalchemy import create_engine
import os

__author__ = "Sreejith Sreekumar"
__email__ = "sreekumar.s@husky.neu.edu"
__version__ = "0.0.1"


cfg = config.read()
host = cfg.get("postgres","host")
database = cfg.get("postgres","database")
user = cfg.get("postgres","user")
password = cfg.get("postgres","password")
tablename = cfg.get("postgres","table")
port = 5432
should_create = cfg.get("postgres","create")



def _getpostgres_connection():
    """
    """
    conn_str = "host={} dbname={} user={} password={}".format(host, database, user, password)
    conn = psycopg2.connect(conn_str)
    
    return conn


def postgres_to_dataframe():
    """

    """
    conn = _getpostgres_connection()
    return pd.read_sql('select * from ' + table, con=conn)



def updated_input_dataframe_to_postgres(df):

    conn = _getpostgres_connection()    
    cur = conn.cursor()

    delete = """Drop table if exists """ + tablename
    cur.execute(delete)
    conn.commit()

    connection_string = "postgresql+psycopg2://" + user + ":" + password + "@" + \
                         host + ":" + str(port) + "/" + database


    engine = create_engine(connection_string)
    df.to_sql(tablename, con=engine)
                     

    

# create table in postgres
# 'CREATE TABLE "similarity"(index1 varchar(20) 
#  NOT NULL, index2 varchar(20) NOT NULL, sim varchar(20) NOT NULL)'

def create_url_info_table():
    """
    
    Arguments:
    - `csv_path`:
    """
    conn = _getpostgres_connection()    
    cur = conn.cursor()

    if(should_create == "yes"):
        delete = """Drop table if exists filings"""
        cur.execute(delete)

        cur.execute("Create Table filings(year text, quarter text, cik text, company text, type text, date text, url text);")
        conn.commit()

    
    cur.close()
    conn.close()



def insert_into_postgres(_year, _quarter, _cik, _company, _type, _date, _url):

    conn = _getpostgres_connection()    
    cur = conn.cursor()

    cur.execute('INSERT into filings(year, quarter, cik, company, type, date, url) VALUES (%s, %s, %s, %s, %s, %s, %s)', [_year, _quarter, _cik, _company, _type, _date, _url])
    
    conn.commit()
    cur.close()
    conn.close()



def insert_batch_into_postgres(rows):

    conn = _getpostgres_connection()    
    cur = conn.cursor()

    
    cur.executemany('INSERT into filings(year, quarter, cik, company, type, date, url) VALUES (%s, %s, %s, %s, %s, %s, %s)', rows)
    
    conn.commit()
    cur.close()
    conn.close()

    
