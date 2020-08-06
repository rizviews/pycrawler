import requests
from bs4 import BeautifulSoup as bs
import logging
import re

class seovalidator(object):
    """description of class"""
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def validate_seo(self,item):
        new_soup = bs(item.content,"html.parser")   
             
        title = new_soup.head.title
        print ("found title is: ",title)
        meta_tags = new_soup.find_all('meta')
        canonical = self.get_canonical_url(new_soup)

        if canonical != '':
            print ("canonical link found: ",canonical)

        site_name = self.extract_site_title_from_meta(meta_tags)
        print ("site name found is: ",site_name)
        if title != None:            
            pattern = "(.*)\s\|\s"+site_name+"</title>"
            pattern = re.compile(pattern)
            matched = re.search(pattern,str(title))
            if matched == None:
                self.logger.error("Page title is not following SEO, found title: %s",title)
            else:
                self.logger.info("Page title is following SEO, found title: %s",matched.group())

    def extract_site_title_from_meta(self,meta_tags):
        site_name = ""
        for meta_tag in meta_tags:
            property = meta_tag.get('property')
            if property=='og:site_name':
                site_name = meta_tag.get('content')
                break
        print ('site title is: ',site_name)        
        self.logger.info('Site name fetched: %s',site_name)
        return site_name

    def get_canonical_url(self,soup):        
        if not soup:
            return ''        

        for link in soup.find_all('link'):            
            rel = link.get('rel')
            if 'canonical' in rel:
                return link.get('href')

        return ''


