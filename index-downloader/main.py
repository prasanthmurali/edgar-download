import urllib.request
import re
import os, shutil

import dbutils

__author__ = "Sreejith Sreekumar"
__email__ = "sreekumar.s@husky.neu.edu"
__version__ = "0.0.1"

text_url_base = "https://www.sec.gov/Archives/"
base_url = "https://www.sec.gov/Archives/edgar/full-index/"
years = list(range(1993, 2018))
quarters = ["QTR1", "QTR2", "QTR3", "QTR4"]

queue = []
batch_size = 10000


def insert_to_db():
    global queue
    print("Inserting next batch of 10000 rows into postgres...")
    dbutils.insert_batch_into_postgres(queue)
    queue = []
    


def process_row(row, year, quarter):
    global queue
    elements = row.split("|")

    try:
        _year = year
        _quarter = quarter
        _cik = elements[-5]
        _company = elements[-4]
        _type = elements[-3]
        _date = elements[-2]
        _url = text_url_base + elements[-1]

        queue.append((_year, _quarter, _cik, _company, _type, _date, _url))

    except:
        pass

    if(len(queue) > batch_size):
        insert_to_db()


def get_url(year, quarter):
    url =  base_url + "/" + str(year) + "/" + quarter + "/" + "master.idx"
    response = urllib.request.urlopen(url)

    html = response.read()
    text = html.decode(encoding='utf-8',errors='ignore')

    text = text.split("--------------------------------------------------------------------------------")[1]
    data_text = text.split("\n")
    rows = data_text[1:len(data_text)]
    text_url_info = [process_row(row, year, quarter) for row in rows]
    insert_to_db()
    


def add_from_quarter(year, quarter):
    url  = get_url(year, quarter)


def add_from_year(year):
    [add_from_quarter(year, quarter) for quarter in quarters]


dbutils.create_url_info_table()    
list(map(add_from_year, years))

