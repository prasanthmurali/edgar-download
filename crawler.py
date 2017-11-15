from bs4 import BeautifulSoup
import re
import requests
import os
import subprocess
from urllib.request import urlopen
from functools import reduce
import config

import shutil
import subprocess, threading

__author__ = "Sreejith Sreekumar"
__email__ = "sreekumar.s@husky.neu.edu"
__version__ = "0.0.1"


cfg = config.read()
base_folder = cfg.get("folder","base")

class Crawler():


    def scrap_filing_documents(self, _type, company_code, cik, priorto, count):

        filing_urls = get_filing_urls(get_base_url(_type, company_code, cik, priorto, count))
        
        documents_collected = []

        for url in filing_urls:
            text_urls = get_filing_htmls(url)
            directory = make_directories_to_store(_type, company_code, priorto, url)

            for text_url in text_urls:

                name_parts = text_url.split("/")
                name = name_parts[len(name_parts) - 1].replace(".htm",".txt")
                
                if name not in documents_collected:
                    html_text = get_text(text_url)
                    save_filing_texts(html_text, directory, name)
                    documents_collected.append(name)
            print("Collected documents from: " + url)
        print("Finished collecting " + _type + " documents for " + company_code)



def get_base_url(_type, company_code, cik, priorto, count):
    """
    
    Arguments:
    - `cik`:
    - `priorto`:
    - `count`:
    """
    base_url = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="+\
                   str(cik) + "&type=" +_type + "&dateb=" + str(priorto)+ "&owner=exclude&"+\
                   "output=xml&count=" + str(count)	

    print("URL for download:", base_url)
    return base_url



def get_filing_urls(base_url):
    """
    
    Arguments:
    - `baseurl`:
    """
    doc = urlopen(base_url).read()
    soup = BeautifulSoup(doc, 'html.parser')
    filing_links = []

    for link in soup.findAll("filinghref"):
        link = str(link).replace("<filinghref>","")
        link = link.replace("</filinghref>","")
        filing_links.append(link)

    return filing_links



def get_filing_htmls(url):
    doc = urlopen(url).read()
    soup = BeautifulSoup(doc, 'html.parser')

    table = soup.find( "table", {"class":"tableFile"} )
    links = table.findAll('a')
    link_pre = "https://www.sec.gov"

    return [link_pre + link['href'] for link in links if link['href'].endswith('htm')]


def make_directories_to_store(_type, company_code, priorto, url):
    
    base_url_parts = url.split("/")
    base_url_index = base_url_parts[len(base_url_parts)-1].replace(".htm","")

    foldername = base_folder + os.sep + _type + os.sep + company_code + os.sep + priorto +\
                                  os.sep + base_url_index 
    
    if os.path.exists(foldername):
        shutil.rmtree(foldername)

    os.makedirs(foldername)
    return foldername


def kill_lynx(pid):
    os.kill(pid, signal.SIGKILL)
    os.waitpid(-1, os.WNOHANG)
    print("lynx killed")


def get_text(url):
    """
    """
    cmd = "lynx -dump -nolist -notitle \"{0}\"".format(url)
    lynx = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    t = threading.Timer(300.0, kill_lynx, args=[lynx.pid])
    t.start()
 
    web_data = lynx.stdout.read()
    t.cancel()
 
    web_data = web_data.decode("utf-8", 'replace')

    return web_data


def save_filing_texts(text, directory, name):

    op_file = directory + os.sep + name
    
    with open(op_file, "w") as f:
        f.write(text)
    


