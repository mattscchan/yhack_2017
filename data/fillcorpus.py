import json
import re
#import urllib2
import urllib.parse
import urllib.request
import codecs
import time


with open("fake_or_real_news.json") as data_files:
    
    doc = json.load(data_files)
    #doc = json.load(codecs.open("fake_or_real_news.json", 'r', 'utf-8-sig'))
    for idx,ex in enumerate(doc):
        time.sleep(3)

        if ex['example'] == u"exmample":
            continue
        #print ex['example'].encode('ascii')
        parsedQuery = ex['target']['title'].split(u' ')

        print (parsedQuery)
        parsedQuery = u"+".join(parsedQuery)
        print (parsedQuery)
        parsedQuery = re.sub(r'<[^<>]*>', u'', parsedQuery)
        print (parsedQuery)
        parsedQuery = re.sub(r'[^a-zA-Z.+ ]', u'', parsedQuery)
        print (parsedQuery)
        mydata = {"q": parsedQuery,
          "mkt": "en-us"}
       # mydata = urllib.parse.urlencode(mydata)
        mydata = mydata.encode('encoding')

        myheaders = {"Ocp-Apim-Subscription-Key": "c87d294a9c8e4effb43d6a3d0ef9859b"}
        req = urllib.request.Request(url="https://api.cognitive.microsoft.com/bing/v7.0/news/search",method='get', data=mydata, headers = myheaders)
        print(req)
        with urllib.request.urlopen(req) as response:
            content = response.read()

        print(content)
        if (idx > 4):
            break