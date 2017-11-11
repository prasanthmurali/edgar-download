from bs4 import BeautifulSoup
import re
import requests
import os
import subprocess
from urllib.request import urlopen
from functools import reduce


__author__ = "Sreejith Sreekumar"
__email__ = "sreekumar.s@husky.neu.edu"
__version__ = "0.0.1"


class Crawler():


    def scrap_filing_documents(self, _type, company_code, cik, priorto, count):

        filing_urls = get_filing_urls(get_base_url(_type, company_code, cik, priorto, count))

        get_filing_htmls(filing_urls[0])
            
           
        
        pass





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
