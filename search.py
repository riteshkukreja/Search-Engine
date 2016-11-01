#!python

import os
import string
from os import listdir
from os.path import basename, isdir, isfile, join
import re
import cgi
import sys
import json

#Lookup
def lookup(index, graph, keywords):
    results = []
    bestresults = []
    popularity = []
    bestpopularity = []
    
    for keyword in keywords:
        keyword = validWord(keyword).lower()
        if keyword in index:
            union(results, index[keyword])
    for keyword in keywords:
        if keyword in index:
            bestresults = intersect(results, index[keyword])

    for url in results:
        if url in graph:
            popularity.append( [graph[url]])

    for url in bestresults:
        if url in graph:
            bestpopularity.append( [graph[url]])


    results = [x for (y,x) in sorted(zip(popularity,results), reverse=True)]
    bestresults = [x for (y,x) in sorted(zip(bestpopularity,bestresults), reverse=True)]
    union(bestresults, results)
    return bestresults


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

# Retrive to file index.txt
def getIndex():
    import json, os
    if os.path.exists("database/index.json"):
        infile = open("database/index.json", "r+")
        index = byteify(json.load(infile))
        infile.close()
        return index
    else:
        return {}

# Retrive to file index.txt
def getGraph():
    import json, os
    if os.path.exists("database/graph.json"):
        infile = open("database/graph.json", "r+")
        graph = byteify(json.load(infile))
        infile.close()
        return graph
    else:
        return {}

# Convert from UNICODE
def byteify(input):
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

#Valid Word
def validWord(word):
    import re
    word = re.sub('[^A-Za-z0-9]+', '', word)
    return word

# Automatic scripts

index = getIndex()
graph = getGraph()


print "Content-type: application/json"
print ""

form = cgi.FieldStorage()
results = []
terms = ""

response = {'success': False, 'data': [], 'error': [], 'status': 404}

try:
    if form.has_key("terms"):
        terms = form.getvalue("terms")
        terms = terms.split()
        results = lookup(index, graph, terms)
        response['data'] = results
        response['success'] = True
        response['status'] = 200
    else:
        response['error'].append("Invalid Params")
except NameError:
    response['error'].append("There was an error understanding your search request.  Please press the back button and try again.")
except:
    response['error'].append("Really Unexpected error:" + sys.exc_info()[0])

print json.dumps(response, ensure_ascii=False)



