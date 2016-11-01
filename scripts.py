#Remove tags before getting  keywords
def removeAllTags(in_text):
        import re

        # get rid of new lines
        in_text = re.sub(r'\s+', ' ', in_text)

        # Remove Menu
        in_text = removeMenu(in_text)

        # Remove Head
        in_text = removeHead(in_text)

        # Remove scripts
        in_text = removeScripts(in_text)

        # Remove forms
        in_text = removeForms(in_text)

        # Remove Comments
        in_text = removeComments(in_text)

        # Remove HTML encoding
        in_text = removeHTMLEncode(in_text)

        # Remove all tags
        p = re.compile(r'<.*?>')
        b = p.sub('', in_text)
        return re.sub('\s+', ' ', b)

def removeTagRegex(page, tag):
    import re
    p = re.compile(r'<\s*?' + tag + '.*?>.*?<\s*?/' + tag + '\s*?>')
    return p.sub('', page)

def removeTagByAttrib(page, attr, value, perfect = True):
    import re
    data = list(page)
    pos = 0
    while True:
        startLink = page.find('<', pos)
        if startLink == -1:
            break
        endLink = page.find('>', startLink+1)

	#find id
        if perfect:
            matches = re.findall(r'' + attr + '(\s+)?=(\s+)?[\'\"]' + value + '[\'\"]', page[startLink:endLink])
        else:
            matches = re.findall(r'' + attr + '(\s+)?=(\s+)?[\'\"](\w+)?' + value + '(\w+)?[\'\"]', page[startLink:endLink])
        if len(matches) > 0:
            #remove entire tag
            #get tag name
            tag = re.findall(r'\w+', page[startLink:endLink])
            tagend = page.find('</' + tag[0] + '>', startLink+1)
            data[startLink: tagend+len(tag) + 3] = ""
            pos = tagend
        else:
            pos = endLink
    return ''.join(data)

def removeTagById(page, id):
    return removeTagByAttrib(page, "id", id)

def removeTagByClass(page, className):
    return removeTagByAttrib(page, "class", className)

def removeScripts(page):
    return removeTagRegex(page, "script")

def removeForms(page):
    return removeTagRegex(page, "form")

def removeHead(page):
    # retriev body tag and replace content with body tag
    import re
    li = re.findall('<\s*?body.*?>(.*)<\s*?/body\s*?>', page)
    if len(li) > 0:
        return li[0]
    else:
        return page
    #return removeTagRegex(page, "head")

def removeComments(page):
    data = list(page)
    while True:
        startLink = page.find('<!--')
        if startLink == -1:
            break
        endLink = page.find('-->', startLink + 1)
        data[startLink:endLink+3] = ""
        page = ''.join(data)
        
    return page

def removeHTMLEncode(page):
    var = ['&amp;', '&lt;', '&gt;', '\\n', '\\t', '&nbsp;']
    import re
    for data in var:
        page = re.sub(r'' + data + '', ' ', page)
    return page

def removeMenu(page):
	page = removeTagRegex(page, "nav")
	page = removeTagByAttrib(page, "id", "menu", False)
	page = removeTagByAttrib(page, "class", "menu", False)
	page = removeTagByAttrib(page, "title", "menu", False)

	return page
