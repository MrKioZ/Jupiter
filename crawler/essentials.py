import requests
from bs4 import BeautifulSoup
from selenium import webdriver

class SitesManager():

    def __init__(self):
        self.browser = webdriver.Firefox(executable_path=r'C:\Utility\BrowserDrivers\geckodriver.exe')

    def __del__(self):
        self.browser.close()

    def get(self,url):
        self.browser.get(url)

    @property
    def page_source(self):
        return self.browser.page_source

    def scrape(self,keywords,type='google'):
        if type.lower() == 'google':
            self.browser.get('https://google.com/search?q='+keywords)
            soup = BeautifulSoup(self.browser.page_source, 'lxml')
            for indx, i in enumerate(soup.findAll('div',{'class':'g'})):
                a = i.find('a', href=True)
                h3 = i.find("h3")
                try:
                    desc = i.find('div',{'class':'s'}).text
                except:
                    continue
                print(h3.text)
                self.insert(h3.text, a['href'], desc)

    def GetKeyWords(self, Url):
        keywords = []
        with self.request(url) as r:
            with BeautifulSoup('lxml') as soup:
                for h in ['h1','h2','h3','h4','h5']:
                    for i in soup.findall(h):
                        if (not i.text in keywords):
                            keywords.append(i.text)
        return keywords
