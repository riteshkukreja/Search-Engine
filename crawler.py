#!/usr/bin/python
import threading
import images
import graph
import index
import methods
import time
import os
from logger import logger as lg

class myThread (threading.Thread):
    def __init__(self, threadID, name, link, event):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.link = link
        self.event = event
    def run(self):
        if self.event.is_set():
            crawl(self.link, self.threadID)
            
    def terminate(self):
        self.event.clear()

def terminate():
    #active()
    global event, logger, threads
    started = False
    event.clear()
    try:
        while threading.activeCount() > 2:
            time.sleep(1)
            logger.log("Waiting on " + str(threading.activeCount()) + " threads")
            for t in threads:
                t.terminate()

        #saveThreads()
        logger.log("Shutting down gracefully")
        status(True)
        os._exit(0)
    except KeyboardInterrupt:
        status(True)
        os._exit(0)
    #print ("Terminated!")

def active():
    print ("========================================================\n")
    print (" Active Threads : " + str(threading.activeCount()) + "\n")
    print ("========================================================\n")

def report():
    global crawled
    global toCrawl
    print ("========================================================\n")
    print (" CRAWLED " + str(len(crawled)) + "\t" + " OF " + str(len(toCrawl)) + "\n")
    print ("========================================================\n")

def status(reset=False):
    import json
    global crawled, toCrawl, imageDict, indexDic, threadCount
    if(reset):
        obj = {'crawled': str(len(crawled)), 'tocrawl': str(len(toCrawl)), 'images': str(len(imageDict)), 'keywords': str(len(indexDic)), 'threads': '0', 'logs': []}
    else:
        obj = {'crawled': str(len(crawled)), 'tocrawl': str(len(toCrawl)), 'images': str(len(imageDict)), 'keywords': str(len(indexDic)), 'threads': str(threading.activeCount()), 'logs': logger.getLogs()}
    logger.clear()
    methods.saveStatus(json.dumps(obj, ensure_ascii=False))

def getID():
    global crawled
    return len(crawled)

def getCrawlID():
    global toCrawl
    return len(toCrawl)

def saveThreads(threads):
    global crawled, toCrawl
    
    for link in threads:
        if link not in crawled:
            toCrawl.append(link)
            methods.addToCrawl(link)


def crawl(url, myid):

    global id
    global indexDic
    global graphDict
    global imageDict
    global crawled
    global lock
    global event
    global toCrawl
    global threadCount

    if(threadCount >= 200):
        logger.alert("Memory limit reached")
        # Add to tocrawl
        saveThreads([url])
        return

    threadCount += 1
    
    if url in crawled:
        threadCount -= 1
        logger.error(url + ": Already Crawled!")
        return

    try:
        content = methods.getPage(url)
        
        if(len(content) == 0):
            # no content
            logger.error(url + ": 404 NOT FOUND!")
        else:
            logger.log(url)

            if event.is_set():
                links = index.getLinks(content)
                links = methods.formattedLinks(links, url)
                            
                lock.acquire()

                if not event.is_set():
                    #if event released in between push to toCrawl and return
                    logger.warn("Saving thread for future crawl: " + url);
                    saveThreads([url])
                    lock.release()
                    return 

                # save as crawled
                logger.log(str(myid) + ": Setting page to crawled")
                crawled.append(url)
                methods.saveCrawled(url)


                # Maintain Index
                logger.log(str(myid) + ": Adding Page to Index")
                index.addPageToIndex(indexDic, url, content)

                # Maintain Images Index
                logger.log(str(myid) + ": Adding Images to Index")
                images.addImagesToIndex(imageDict, url, content)

                # Maintain Graph Links and Ratings
                logger.log(str(myid) + ": Adding Page to Graph")
                graph.graph(graphDict, url, links)
                
                lock.release()

                if event.is_set():
                    logger.log("Starting " + str(len(links)) + " threads")
                    for link in links:
                        if link not in crawled:
                            thread = myThread(id, "Thread-" + str(id), link, event)
                            threads.append(thread)
                            thread.start()
                            thread.setDaemon = False
                            #thread.join()
                            id += 1
                else:
                    logger.log("Saving " + str(len(links)) + " links to file")
                    saveThreads(links)
                
            else:
                logger.warn("Adding " + url + " to crawl list")
                saveThreads([url])
        threadCount -= 1

    except KeyboardInterrupt:
        saveThreads([url])
        logger.error(url + ": KeyboardInterrupt Exception")
        threadCount -= 1
        terminate()

id = 1
threadCount = 0
started = False
logger = lg()
crawled = methods.getCrawled()
toCrawl = methods.getToCrawl()


threads = []
lock = threading.Lock()
event = threading.Event()
event.set()

indexDic = index.getIndex()
graphDict = graph.getGraphLinks()
imageDict = images.getImagesFile()

class Sleeper (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.event.set()
    def run(self):
        if self.event.is_set():
            try:
                while self.event.is_set():
                    time.sleep(1)
                    lock.acquire()
                    status()
                    lock.release()
            except:
                self.event.clear()
                terminate()
            
    def terminate(self):
        self.event.clear()


def Main():
    global id
    global toCrawl
    global event, started, logger

    started = True
    logger.log("Booting up...")

    try:
        for url in toCrawl:
            # Create new threads
            toCrawl.remove(url)
            thread1 = myThread(id, "Thread-" + str(id), url, event)
            id += 1
            thread1.setDaemon = False
            # Start new Threads
            thread1.start()
            #thread1.join()
        methods.saveToCrawl(toCrawl)
    except KeyboardInterrupt:
        print ("Terminating")
        terminate()

    sleeperThread = Sleeper()
    sleeperThread.setDaemon = False
    sleeperThread.start()
    raw_input()


# and thus it began the journey
Main()