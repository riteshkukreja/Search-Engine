import methods

# Get Images
def getNextImage(page):
    startLink = page.find('<img')
    if startLink == -1:
        return None, 0
    
    closingTag = page.find('>', startLink)
    tag = page[startLink: closingTag+1]

    src = tag.find('src')
    if src == -1:
        page = page[closingTag:]
        return getNextImage(page)
    
    startQuote = tag.find('"', src)
    endQuote = tag.find('"', startQuote + 1)

    if startQuote == -1:
        startQuote = tag.find('\'',src)
        endQuote = tag.find('\'',startQuote + 1)
    
    url = tag[startQuote + 1 : endQuote]

    # get alternate text
    alt = tag.find('alt')
    if alt == -1:
        return url , '', closingTag
    
    startQuote = tag.find('"', alt)
    endQuote = tag.find('"', startQuote + 1)

    if startQuote == -1:
        startQuote = tag.find('\'',alt)
        endQuote = tag.find('\'',startQuote + 1)
    
    altText = tag[startQuote + 1 : endQuote]
    
    
    return url, altText, closingTag

# Get Images from a page
def getImages(page, domain):
    images = []
    while True:
        try:
            url, altText, endpos = getNextImage(page)
            if url:
                if methods.validURL(url):
                    tags = altText.split()
                    for w in tags:
                        w = methods.validWord(w.lower())
                        
                    imgName = url.rsplit('/', 1)[-1]
                    imgType = imgName.rsplit('.', 1)[-1]
                    imgName = imgName.rsplit('.', 1)[0]

                    methods.union(tags, [imgName])

                    url = methods.formattedLinks([url], domain)[0]

                    temp = {}
                    temp['url'] = url
                    temp['name'] = imgName
                    temp['type'] = imgType
                    
                    methods.union(images ,[[temp, tags]])
                
                page = page[endpos + 1:]
            else:
                break
        except:
            break
    return images

# Add images to Index
def addImagesToIndex(imagedex, url, page):
    if not methods.validURL(url):
        return
    url = methods.validURL(url)
    images = getImages(page, url)
    for image in images:
        tags = image[1]
        for tag in tags:
            addListToIndex(imagedex, tag.lower(), image[0])

    saveImagesFile(imagedex)

# Add List to Index
def addListToIndex(index, keyword, url):
    if keyword in index:
        methods.union(index[keyword], [url])
        return
    else:
        index[keyword] =  [url]



#======================FILE MANAGEMENT======================#


# Write to file index.txt
def saveImagesFile(image):
    import json
    outfile = open("database/images.json", "w+")
    json.dump(image, outfile, indent=4)
    outfile.close()

# Retrive to file index.txt
def getImagesFile():
    import json, os
    if os.path.exists("database/images.json"):
        infile = open("database/images.json", "r+")
        image = methods.byteify(json.load(infile))
        infile.close()
        return image
    else:
        return {}
