import requests
import json
from bs4 import BeautifulSoup as BS
from loguru import logger
from config import URL

def get_all_flatlinks():
    k = 1
    r = requests.get(URL+str(k))
    # logger.debug(r)
    links = []
    while r.url == URL+str(k):
        
        html = BS(r.content, 'html.parser')

        search_panel = html.find("div", {"id": "domSearchPanel"})
        #logger.debug(search_panel)
        for section in search_panel.find_all('section'):
            #logger.debug(f'1 - {section}')
            if 'sold' not in section['class']:
                #logger.debug('Not sold')
                #logger.debug(f'2 - {section}')
                div = section.find_all('div', {'class':'main-photo'})[0]
                
                link = f"https://dom.ria.com{div.find_all('a')[0]['href']}"
                #logger.debug(link)
                links.append(link)

        k += 1
        r = requests.get(URL+str(k))
        
    return links


if __name__ == "__main__":
    links = get_all_flatlinks()
    print(links)
    print('ended')