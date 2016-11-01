import re
from collections import Counter
from bitmap  import Bitmap
from hashlib import md5

WORDS = Counter([])
bmap = Bitmap(2**20)

def makeHashes(word) :
    # convert 32 hexdigits to list of 6 hash keys
    hex32 = md5(word).hexdigest()
    hashes = []
    for i in range(0,30,5) :
        hashes.append(int(hex32[i:i+5],16))
    return hashes

def loadBitmap(file) :
    # generate bitmap from lexicon file (one word per line)
    words = open(file).readlines()
    words = map(lambda x: x.strip(), words) # no newlines please
    for word in words :
        hashes = makeHashes(word)
        for hash in hashes :
            bmap.setBit(hash)
   # return bmap

def setWord(word):
    hashes = makeHashes(word)
    for hash in hashes :
        bmap.setBit(hash)

def checkWord(word) :
    # return True if word in lexicon
    hashes = makeHashes(word)
    for hash in hashes :
        if not bmap.getBit(hash): return False
    return True

def words(text): 
    return re.findall(r'\w+', text.lower())

def P(word): 
    "Probability of `word`."
    N=sum(WORDS.values())
    return WORDS[word] / float(N)

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    #return (known([word]) or known(edits1(word)) or known(edits2(word)) or known(editsN(word, 3)) or [word])
    return (known([word]) or known(edits1(word)) or known(editsN(word, 2)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def editsN(word, N): 
    "All edits that are N edits away from `word`."
    L = edits1(word)
    if(N == 1): 
        return L

    for i in range(N-1):
        H = (e2 for e1 in L for e2 in edits1(e1))
        L = H

    return L

def check(text):
    words = re.sub("[^a-zA-Z'-]"," ",text).lower().split()
    for key in range(len(words)):
        if len(words[key]) < 3:
            words[key] = ''
            continue;

        if not checkWord(words[key]):
            newword = correction(words[key])
            if words[key] == newword:
                # add to db
                WORDS.update([newword])
                setWord(newword)
            
            words[key] = newword
    
    return ' '.join(words)

def loadJSONFile(file):
    import json
    data = {}

    with open(file) as data_file:    
        data = json.load(data_file)
    return data


WORDS = Counter(loadJSONFile("database/frequency.json"))
loadBitmap("database/spell.words")