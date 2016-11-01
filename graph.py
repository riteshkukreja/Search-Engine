import methods

# ranker
def computeRanks(graph):
    d = 0.8
    n = 10
    
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages

    for i in range(0, n):
        newranks = {}
        for page in graph:
            newrank = (1 - d)  / npages
            for node in graph:
                if page in graph[node]:
                    newrank += d * (ranks[node] / len(graph[node]))
            newranks[page] = newrank
        ranks = newranks
    return ranks

# Graph Method to maintain dictionary
def graph(graphDict, url, links):
    if links:
        graphDict[url] = links
    saveGraphLinks(graphDict)
    ratedDict = computeRanks(graphDict)
    saveGraph(ratedDict)

#======================FILE MANAGEMENT======================#


# Write to file index.txt
def saveGraph(graph):
    import json
    outfile = open("database/graph.json", "w+")
    json.dump(graph, outfile, indent=4)
    outfile.close()

# Retrive to file index.txt
def getGraph():
    import json, os
    if os.path.exists("database/graph.json"):
        infile = open("database/graph.json", "r+")
        graph = methods.byteify(json.load(infile))
        infile.close()
        return graph
    else:
        return {}

# Write to file index.txt
def saveGraphLinks(graph):
    import json
    outfile = open("database/links.json", "w+")
    json.dump(graph, outfile, indent=4)
    outfile.close()

# Retrive to file index.txt
def getGraphLinks():
    import json, os
    if os.path.exists("database/links.json"):
        infile = open("database/links.json", "r+")
        graph = methods.byteify(json.load(infile))
        infile.close()
        return graph
    else:
        return {}
