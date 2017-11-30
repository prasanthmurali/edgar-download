import config
import urllib.request
import re
import os, shutil

__author__ = "Sreejith Sreekumar"
__email__ = "sreekumar.s@husky.neu.edu"
__version__ = "0.0.1"


cfg = config.read()

base_url = "https://www.sec.gov/Archives/edgar/full-index"
years = cfg.get("filing","years").split(",")
quarters = cfg.get("filing","quarters").split(",")

text_base_url = "https://www.sec.gov/Archives"
base_folder = cfg.get("folder","base")



def collect_and_store_text(url_info, year, quarter):

    if len(url_info) == 4:

        foldername = get_folder_name(year, quarter)

        try:
            url = url_info[len(url_info)-1]


            html = urllib.request.urlopen(url).read()
            text = html.decode(encoding='utf-8',errors='ignore')

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
            print(e)
            print("Error collecting :", url)



def get_folder_name(year, quarter):
    return base_folder + os.sep + year + os.sep + quarter

def make_directories_to_store(year, quarter):
    
    foldername = get_folder_name(year, quarter)

    if os.path.exists(foldername):
        shutil.rmtree(foldername)

    os.makedirs(foldername)
    return foldername



def get_text_urls(row):
    """
    
    Arguments:
    - `url`:
    """
    parts = re.split(" +", row.strip())

    length = len(parts)
    
    try:
        form_type = parts[length-4].strip()
        cik = parts[length-3].strip()
        date = parts[length-2].strip()

        end_part = parts[length-1]
        return [form_type, cik, date, text_base_url + "/" + end_part]
    except:
        return []    
    
    


def get_urls():
    """
    """

    urls = []
    
    for idx in range(len(years)):
        url = base_url + "/" + years[idx] + "/" + quarters[idx] + "/" + "company.idx"
        print("Collecting index from URL: ", url)
        response = urllib.request.urlopen(url)
        
        html = response.read()
        text = html.decode(encoding='utf-8',errors='ignore')

        text = text.split("---------------------------------------------------------------------------------------------------------------------------------------------")[1]
        data_text = text.split("\n")
        rows = data_text[1:len(data_text)]
        text_url_info = [get_text_urls(row) for row in rows]

        make_directories_to_store(years[idx], quarters[idx])
        [collect_and_store_text(url_info, years[idx], quarters[idx]) for url_info in text_url_info]
    pass


print(get_urls())
