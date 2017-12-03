import json
import re
#import urllib2
import urllib.parse
import urllib.request
import codecs
import time
import lxml.html
from bs4 import BeautifulSoup#from HTMLParser import HTMLParser


with open("fake_or_real_news.json", encoding="utf8") as data_files:
    
    doc = json.load(data_files)
    #doc = json.load(codecs.open("fake_or_real_news.json", 'r', 'utf-8-sig'))
    for idx,ex in enumerate(doc):
        time.sleep(3)

        if ex['example'] == u"exmample":
            continue
        #print ex['example'].encode('ascii')
        parsedQuery = ex['target']['title'].split(u' ')

        parsedQuery = u"+".join(parsedQuery)
        parsedQuery = re.sub(r'<[^<>]*>', u'', parsedQuery)
        parsedQuery = re.sub(r'[^a-zA-Z.+ ]', u'', parsedQuery)
        mydata = {"q": parsedQuery,
          "mkt": "en-us"}
        mydata = urllib.parse.urlencode(mydata)
        mydata = mydata.encode('utf-8')
        myheaders = {"Ocp-Apim-Subscription-Key": "c87d294a9c8e4effb43d6a3d0ef9859b"}
        myurl = "https://api.cognitive.microsoft.com/bing/v7.0/news/search" + "?q=" + parsedQuery + "&mkt=en-us"
        req = urllib.request.Request(method='GET', url=myurl, headers = myheaders)
        print(req)
        with urllib.request.urlopen(req) as response:
            content = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))

        allArticles = []
        for i in range(len(content["value"])):
            print(content["value"][i]["url"])
            req = urllib.request.Request( url=content["value"][i]["url"])
            try:
                with urllib.request.urlopen(req) as response:
                    htmlRaw = (response.read().decode(response.info().get_param('charset') or 'utf-8'))
                    article = []
                    #print(htmlRaw)
                    #soup = BeautifulSoup.BeautifulSoup(htmlRaw)
                    soup = BeautifulSoup(htmlRaw, 'html.parser')
                    for anchor in soup.findAll('p'):
                        if (anchor.string != None):
                            article.append(anchor.string.encode('utf-8'))
                            #print (anchor.string.encode('utf-8'))
            except urllib.error.HTTPError :
                print ("too bad")
            allArticles.append(article)
        ex['blob'] = allArticles
        with open("fake_or_real_news.json", 'wb') as outfile:
            json.dump(doc, outfile)

        if (idx > 4):
            
            break