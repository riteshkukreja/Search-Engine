import methods
import scripts

# get all meta tags
def getMeta(content, endPos, metas):
    start = content.find('<meta', endPos)
    if(start != -1):
        end  = content.find('>', start+1)
        methods.union(metas, [ content[start: end+1]])
        return getMeta(content, end+1, metas)
    return metas

# Get Keywords, Author name, Description specified by the developer
def getHeaderTags(page, tag):
    tags = getMeta(page, 0, [])
    for i in tags:
        loc = i.find(tag)
        if loc != -1:
            d = i.find('content', loc)
            if d != -1:
                start = i.find('"', d)
                end = i.find('"', start+1)
                return i[start:end+1]
    
    return ''


