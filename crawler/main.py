from essentials import SitesManager
from bs4 import BeautifulSoup
import os, json,time
# from datetime import datetime
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jupiter.settings")
# from jupiter.models import Query


class JupiterSpider(object):

    def __init__(self, name=None, urls=None):

        self.name = name
        self.urls = urls

        self.sitesmanager = SitesManager()

        self.memory = {}

        if (not name) and (not urls):
            for i in os.listdir():
                if '.json' in i:
                    with open(i,'rb') as conf:
                        data = json.load(conf)
                        self.name = data[0]
                        self.urls = data[1]
                        self.memory = data[2]

    def __del__(self):
        data = [self.name,self.urls, self.memory]
        with open('conf.json','w') as f:
            json.dump(data, f)

    def crawl(self):
        for url in self.urls:
            if not url in self.memory.keys():
                Instructions = self.ExtractInstructions(url)
            else:
                print('Already have instructions for ' + url)
                continue

            if not Instructions['Crawl']:
                self.memory[url] = False
                continue
            else:
                self.memory[url] = Instructions

            print(Instructions)

            for i in Instructions.keys():
                if i == 'Sitemap':
                    for Sitemap in Instructions[i]:
                        XmlDict = self.ReadSitemap(Sitemap)
                        print(XmlDict)

    def AlexaRanking(self, url):
        with self.request('http://data.alexa.com/data?cli=10&dat=s&url='+url.replace('https://','').replace('http://','')) as r:
            r = r.text
        return BeautifulSoup(r, "lxml").find("reach")['rank']

    def ReadSitemap(self, url):
        self.sitesmanager.get(url)
        xml = self.sitesmanager.page_source
        soup = BeautifulSoup(xml)
        sitemapTags = soup.find_all("sitemap")
        for sitemap in sitemapTags:
            xmlDict[sitemap.findNext("loc").text] = sitemap.findNext("lastmod").text

        return xmlDict

    def ExtractUrls(self, url):
        with self.request(url) as r:
            with BeautifulSoup(r.text, 'html.parse') as soup:
                urls = []
                for i in soup.findAll('a'):
                    if ('http://' in i) in ('https://' in i) or ('www.' in i):
                        if url.split('.')[1]+'.'+url.split('.')[2] != i:
                            self.urls.append(i.get('href'))

    def ExtractKeyWords(self, url):
        keywords = []
        with self.request(url) as r:
            with BeautifulSoup('lxml') as soup:
                for h in ['h1','h2','h3','h4','h5']:
                    for i in soup.findall(h):
                        if (not i.text in keywords):
                            keywords.append(i.text)
        return keywords

    # def insert(self, title, url, desc):
    #     query = Query(Keywords=self.GetKeyWords(url),Url=url, title=title, Description=desc, Alexa_Rank=self.AlexaRanking(url))
    #     query.save()
    #     print(title,'has been added to the database')

    def ExtractInstructions(self, url):
        if url.endswith('/'):
            url += 'robots.txt'
        else:
            url += '/robots.txt'

        data = {}
        self.sitesmanager.get(url)
        r = self.sitesmanager.page_source
        soup = BeautifulSoup(r,'lxml')
        pre = soup.find('pre')

        if pre is None:
            print('[*] print not Instructions found in',url)
            data['Crawl'] = False
            return data

        r = pre.text.split('\n')

        for i in r:
            if i.startswith('#'):
                continue
            if 'User-agent' in i:
                if (i.split(': ')[1].replace('\n','') == '*') or (i.split(': ')[1].replace('\n','') == '*'):
                    data['Crawl'] = True
                else:
                    data['Crawl'] = False
            elif 'Disallow' in i:
                try:
                    if i.split(': ')[1] == '/':
                        data['Crawl'] = False
                        return data
                except:
                    data['Crawl'] = False
                    return data

                try:
                    data['Disallow'].append(i.split(': ')[1])
                except:
                    data['Disallow'] = []
                    data['Disallow'].append(i.split(': ')[1])

            elif 'Sitemap' in i:
                url = i.split(': ')[1]
                print('[*] A Sitemap was found',url)

                try:
                    data['Sitemap'].append(url)
                except:
                    data['Sitemap'] = []
                    data['Sitemap'].append(url)

                data['Crawl'] = True
            elif 'Allow' in i:
                try:
                    data['Allow'].append(i.split(': ')[1])
                except:
                    data['Allow'] = []
                    data['Allow'].append(i.split(': ')[1])

                data['Crawl'] = True

        return data

def crawl():
    Spider = JupiterSpider('Jupiterbot', ['http://google.com','http://youtube.com', 'http://facebook.com', 'http://instagram.com', 'http://wikipedia.com'])
    Spider.crawl()

if __name__ == '__main__':
    crawl()
