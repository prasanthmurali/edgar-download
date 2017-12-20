import os
import connector
import config
import urllib.request
import re
import shutil

import string
from bs4 import BeautifulSoup

__author__ = "Sreejith Sreekumar"
__email__ = "sreekumar.s@husky.neu.edu"
__version__ = "0.0.1"


conn = None
batch_size = 1000
cfg = config.read()
foldername = cfg.get("data","location")

def get_connection():

    global conn
    
    if conn is None:
        conn = connector._getpostgres_connection()
    
    return conn



def make_folder_to_store(foldername):
    
    if os.path.exists(foldername):
        shutil.rmtree(foldername)

    os.makedirs(foldername)



def get_readable_text(raw_html):
    raw_html = bytes(raw_html, 'utf-16').decode("utf-16", 'ignore')
    cleantext = BeautifulSoup(raw_html).text
    return cleantext


def crawl(url):

    try:

        html = urllib.request.urlopen(url).read()
        text = html.decode(encoding='utf-8',errors='ignore')

        text = get_readable_text(text)

        filename = url.split("/")[-1]

        filename = foldername + os.sep + filename

        with open(filename, "w") as f:
            f.write(text)

    except:
        print("Couldn't crawl url:", url)
    


def get_urls_between_indices(start_index):
    conn = get_connection()
    cur = conn.cursor()

    print("Start Index:", start_index)
    cur.execute("SELECT url FROM filings offset " + str(start_index) + " limit " + str(batch_size))

    for record in cur:
        crawl(record[0])


def get_count(tablename):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("select count(*) from " + tablename)

    count = 0

    for record in cur:
        count = record[0]

    return count




make_folder_to_store(foldername)


count = get_count("filings")
cut_off = int(count/batch_size)


for i in range(0, cut_off, batch_size):
    get_urls_between_indices(i)

batch_size = count % batch_size
final_batch_start_index = count - batch_size
get_urls_between_indices(final_batch_start_index)    
