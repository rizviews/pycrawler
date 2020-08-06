import requests
from bs4 import BeautifulSoup as bs
import logging
import re
from seovalidator import seovalidator

class pycrawler(object):
    def __init__(self,**kwargs):
        self.url = kwargs['url']    
        logging.basicConfig(format='%(levelname)s:%(message)s',filename='pycrawler.log',level=logging.ERROR)   
        self.seo_validator =  seovalidator()
        
    def crawl(self):
        page = requests.get(self.url)
        soup = bs(page.content,"html.parser")
        logging.info("Crawling initiated")
        #print(soup.prettify())

        anchor_list = soup.find_all('a',limit=15)
        meta_tags = soup.find_all('meta')

        logging.info('Grabing og:site_name for the homepage')
        site_name = self.seo_validator.extract_site_title_from_meta(meta_tags)

        for anchor in anchor_list:
            href = anchor.get('href')
            print (href)
            if href != None:
                if href.find('http')>-1:
                    link = requests.get(href)
                    print("status is: ",link.status_code)
                    if link.status_code != 200:
                        print ("not expected")
                        logging.error("Status is not as per expected. should be 200 but found %s",link.status_code)
                    self.seo_validator.validate_seo(link)

 

