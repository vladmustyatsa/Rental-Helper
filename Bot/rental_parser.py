import requests
import json
from bs4 import BeautifulSoup as BS
from loguru import logger
from config import URL_TEMPLATE


def get_all_flatlinks(city):

    '''
    
    A function which returns links of all apartment rental advertisements 
    in the given city posted on dom.ria.com
    
    '''
    k = 1 # page counter
    url = URL_TEMPLATE.format(city, k)
    r = requests.get(url)
    
    links = []
    logger.info(r.url)
    logger.info(url)
    while r.url == url:
        
        html = BS(r.content, 'html.parser')
        search_panel = html.find("div", {"id": "domSearchPanel"})
        
        for section in search_panel.find_all('section'):
            if 'sold' not in section['class']: # if not rented yet
                divs = section.find_all('div', {'class':'main-photo'})
                if divs:
                    div = divs[0]
                    href_a = div.find_all('a')[0]['href']
                    link = f"https://dom.ria.com{href_a}"
                    links.append(link)

        k += 1
        url = URL_TEMPLATE.format(city, k)
        r = requests.get(url)
        
    return links

if __name__ == "__main__":
    print(get_all_flatlinks('ternopil'))