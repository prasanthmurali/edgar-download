import urllib.request
import re
import os, shutil
import config

import string
from bs4 import BeautifulSoup

__author__ = "Sreejith Sreekumar"
__email__ = "sreekumar.s@husky.neu.edu"
__version__ = "0.0.1"


cfg = config.read()

rows_to_insert = []
quarters = ['QTR1','QTR2','QTR3','QTR4']


filter_string = cfg.get("archive","filters")
base_folder = cfg.get("folder","base")



text_base_url = "https://www.sec.gov/Archives"
base_url = "https://www.sec.gov/Archives/edgar/full-index"

def get_readable_text(raw_html):
    raw_html = bytes(raw_html, 'utf-16').decode("utf-16", 'ignore')
    cleantext = BeautifulSoup(raw_html).text
    return cleantext





def collect_and_store_text(url_info, year, quarter):

    if len(url_info) == 4:

        foldername = get_folder_name(year, quarter)

        try:
            url = url_info[len(url_info)-1]


            html = urllib.request.urlopen(url).read()
            text = html.decode(encoding='utf-8',errors='ignore')

            text = get_readable_text(text)

            file_type = url_info[0]
            cik = url_info[1]
            date = url_info[2]

            url_parts = url_info[3].split("/")
            filename = "".join(url_parts[len(url_parts) - 2:])

            filepath = foldername + os.sep + file_type + os.sep + cik + os.sep + date
            os.makedirs(filepath)


            file_to_write = filepath + os.sep + filename

            if os.path.isfile(file_to_write):
                os.remove(file_to_write)



            with open(file_to_write, "w") as f:
                f.write(text)


        except Exception as e:
            pass
    

def get_text_urls(row):


    parts = re.split(" +", row.strip())

    length = len(parts)

    try:
        form_type = parts[length-4].strip()
        cik = parts[length-3].strip()
        date = parts[length-2].strip()

        end_part = parts[length-1]

        return [form_type, cik, date, text_base_url + "/" + end_part]
    except:
        print("Error in an entry in the index, skipping...")
        return []



def get_folder_name(year, quarter):
    return base_folder + os.sep + year + os.sep + quarter


def make_directories_to_store(year, quarter):

    foldername = get_folder_name(year, quarter)

    if os.path.exists(foldername):
        shutil.rmtree(foldername)

    os.makedirs(foldername)
    return foldername



def make_url(parts):

    year = parts[0]
    quarter = parts[1]

    filing_type = None


    if(len(parts) > 2):
        if(parts[2].strip() != ""):
            filing_type = parts[2]

    cik = None

    if(len(parts) > 3):
        cik = parts[3]

    if(quarter.strip() == ""):
        [collect_data_for_year_and_quarter(cik, quarter, year, parts, filing_type) for quarter in quarters]
    else:
        collect_data_for_year_and_quarter(cik, quarter, year, parts, filing_type)

    
def collect_data_for_year_and_quarter(cik, quarter, year, parts, filing_type):

    url = base_url + "/" + year + "/" + quarter + "/" + "company.idx"

    print("Collecting index from URL: ", url)
    response = urllib.request.urlopen(url)

    html = response.read()
    text = html.decode(encoding='utf-8',errors='ignore')

    text = text.split("---------------------------------------------------------------------------------------------------------------------------------------------")[1]
    data_text = text.split("\n")
    rows = data_text[1:len(data_text)]
    if cik is None:
        text_url_info = [get_text_urls(row) for row in rows]
    else:
        text_url_info = [get_text_urls(row) for row in rows if cik in row]


    if filing_type is not None:
        text_url_info = [info for info in text_url_info if len(info) > 0 and info[0] == filing_type]

    make_directories_to_store(year, quarter)
    [collect_and_store_text(url_info, year, quarter) for url_info in text_url_info]




def get_urls_from_filters(filter_string):
    parts_list = [url_parts.split(":") for url_parts in filter_string.split(";")]
    [make_url(parts) for parts in parts_list]
