from crawler import Crawler
import config

__author__ = "Sreejith Sreekumar"
__email__ = "sreekumar.s@husky.neu.edu"
__version__ = "0.0.1"


'''
   Sec-edgar downloads: https://github.com/rahulrrixe/sec-edgar
'''

cfg = config.read()
company_codes = cfg.get("filing","companycodes").split(",")
filing_types = cfg.get("filing","filing_types").split(",")
ciks = cfg.get("filing","ciks").split(",")
priortos = cfg.get("filing","priortos").split(",")
counts = cfg.get("filing","counts").split(",")

crawler = Crawler()

    


def get_filings(filing_types, company_codes, ciks, priortos, counts):

    for company_code, filing_type, cik, priorto, count in zip(filing_types, company_codes,
                                                              ciks, priortos, counts):

        crawler.scrap_filing_documents(company_code, filing_type, cik, priorto, count)
        print("Downloading for company"+ str(company_code) +  "done")

    
#if __name__ == '__main__':
get_filings(filing_types, 
              company_codes,                     
              ciks, 
              priortos, 
              counts)



