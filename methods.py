import scripts

# get page off the internet
def getPage(url):
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ""

#Valid Word
def validWord(word):
    import re
    word = re.sub('[^A-Za-z0-9]+', '', word)
    return word

#union
def union(s1,s2):
    for s in s2:
        if s not in s1:
            s1.append(s)

#intersection
def intersect(s1,s2):
    s3 = []
    for s in s2:
        if s in s1:
            s3.append(s)
    return s3


# Valid URL
def validURL(url):
    if "mailto:" in url:
        return None
    if "{" in url:
        return None
    if "}" in url:
        return None
    if "[" in url:
        return None
    if "]" in url:
        return None
    if "#" in url:
        pos = url.find('#', 0)
        url = url[0:pos]
        return url
    if "javascript" in url:
        return None
    if isinstance(url, str):
        return url
    return None

# Format links
def formattedLinks(links, url):
    from urlparse import urlparse
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    myLinks = []
    for link in links:
        link = formatLink(link, domain, url)
        union(myLinks, [link])
    return myLinks

# format single link
def formatLink(link, domain, url):
    if link[0:7] == 'http://':
        return link
    elif link[0:8] == 'https://':
        return link
    elif link[0:2] == '//':
        if domain[0:7] == 'http://':
            link = 'http:' + link
        else:
            link = 'https:' + link
        return link
    elif link[0:1] == '/':
        if domain[-1] == '/':
            link = domain + link[1:]
        else:
            link = domain + link
        return link
    elif link[0:7] == 'mailto:':
        link = '[' + link +']'
        return link
    elif link[0:3] == '../':
        pos = url.rfind('/')
        link = link[3:]
        return formatLink(link, domain, url)
    elif link[0:1] == '.':
        link = domain + link[1:]
        return link
    else:
        if domain[-1] == '/':
            link = domain + link
        else:
            link = domain + '/' + link
        return link

# Convert from UNICODE
def byteify(input):
    if isinstance(input, dict):
        return {byteify(key):byteify(input[key]) for key in input}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, str):
        return input.encode('utf-8')
    else:
        return input

# Manage crawled URLS
def saveCrawled(url):
    with open("database/crawled.txt", "a") as text_file:
        text_file.write("{}\n".format(url))

def getCrawled():
    try:
        with open("database/crawled.txt") as link:
            lines = link.read().splitlines()
        return lines
    except:
        return []

# Manage TO Crawl List
def addToCrawl(url):
    with open("database/tocrawl.txt", "a") as text_file:
        text_file.write("{}\n".format(url))

def saveToCrawl(data):
     with open("database/tocrawl.txt", "wb") as text_file:
         for  item in data:
             text_file.write("%s\n" % item)

def getToCrawl():
    try:
        with open("database/tocrawl.txt") as link:
            lines = link.read().splitlines()
        return lines
    except:
        return []

def saveStatus(data):
     with open("database/status.txt", "wb") as text_file:
        text_file.write("%s" % data)

def getStatus():
    try:
        with open("database/status.txt", "rb") as text_file:
            lines = text_file.read()
            return lines
    except:
        return ""