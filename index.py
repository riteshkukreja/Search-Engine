import header
import methods
from time import time
import re
import SpellChecker
import scripts

# Get Next Target URLs
def getNextTarget(page):
    startLink = page.find('<a href=')
    if startLink == -1:
        return None, 0
    href = page.find('href', startLink)
    closingTag = page.find('>', startLink)
    if closingTag < href:
        page = page[closingTag:]
        return getNextTarget(page)
    startQuote = page.find('"', href)
    endQuote = page.find('"', startQuote + 1)
    url = page[startQuote + 1 : endQuote]
    return url, endQuote

# Get Links from a page
def getLinks(page):
    links = []
    while True:
        try:
            url, endpos = getNextTarget(page)
            if url:
                if methods.validURL(url):
                    methods.union(links ,[url])
                
                page = page[endpos + 1:]
            else:
                break
        except:
            break
    return links

# Add websites details
def addWebsiteDetails(obj):
    websites = getWebsite()
    if obj['url'] in websites:
        if obj['crawled'] > websites[obj['url']]['crawled']:
            # update info
            websites[obj['url']] = obj
        else:
            pass
    else:
        websites[obj['url']] = obj
    saveWebsite(websites)

# Add to Index
def addToIndex(index, keyword, urlobj):
    if keyword in index:
        if urlobj['url'] in index[keyword]:
            methods.union(index[keyword][urlobj['url']]['position'], urlobj['position'])
            index[keyword][urlobj['url']]['count'] = len(index[keyword][urlobj['url']]['position'])
        else:
            index[keyword][urlobj['url']] = urlobj
        return
    else:
        index[keyword] =  {}
        index[keyword][urlobj['url']] = urlobj

def addPageToIndex(index, url, content):
    #url = formatLink(url)

    if not methods.validURL(url):
        return

    print "Starting Indexing"
    url = methods.validURL(url)
    specifiesKeywords = header.getHeaderTags(content, 'keywords')
    author = header.getHeaderTags(content, 'author')
    description = header.getHeaderTags(content, 'description')
    

    print "Starting Tags Removal"
    content = scripts.removeAllTags(content)
    content = re.sub(r'[^a-zA-Z0-9]+', " ", content)
    content = re.sub(r'\s+', " ", content)

    #content = SpellChecker.check(content)
    #specifiesKeywords = SpellChecker.check(specifiesKeywords)

    print "Starting Context Splicing"
    words = content.split()
    keywords = specifiesKeywords.split()

    urlFormatted = {}
    urlFormatted['url'] = url
    urlFormatted['author'] = author
    urlFormatted['description'] = description
    urlFormatted['keywords'] = specifiesKeywords
    urlFormatted['content'] = content
    urlFormatted['crawled'] = time()
    urlFormatted['updateTime'] = 1000000

    addWebsiteDetails(urlFormatted)
    
    #methods.union(words, keywords)
    pos = 0
    print "Starting Adding to Index"
    for word in words:
        if(len(word) >= 3):
            #word = header.removeHeader(word)
            #word = methods.validWord(word)
            addToIndex(index, word.lower(), {'url':url, 'position':[pos], 'count':1})
        pos += 1
    saveIndex(index)


#======================FILE MANAGEMENT======================#

# Write to file index.json
def saveIndex(index):
    import json
    outfile = open("database/index.json", "w+")
    json.dump(index, outfile, indent=4)
    outfile.close()

# Retrive to file index.json
def getIndex():
    import json, os
    if os.path.exists("database/index.json"):
        infile = open("database/index.json", "r+")
        index = methods.byteify(json.load(infile))
        infile.close()
        return index
    else:
        return {}

# Write to file websites.json
def saveWebsite(website):
    import json
    outfile = open("database/website.json", "w+")
    json.dump(website, outfile, indent=4)
    outfile.close()

# Retrive to file website.json
def getWebsite():
    import json, os
    if os.path.exists("database/website.json"):
        infile = open("database/website.json", "r+")
        website = methods.byteify(json.load(infile))
        infile.close()
        return website
    else:
        return {}

#=================== INIT commands ========================
