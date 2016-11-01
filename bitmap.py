# bitmap.py - define the class bitmap

class Bitmap :
  def __init__(self, nBits, wordSize=16) :
    self.nBits = nBits
    self.wordSize = wordSize
    self.nWords = (nBits+self.wordSize-1)/self.wordSize
    self.masks  = []    # 2**n for n = 1..16 (bit to set or get)
    self.nSet   = 0     # Bits actually set in the map

    # set masks to [1,2,4,8,..,32768] powers of 2
    bit = 1
    for i in range(self.wordSize) :
        self.masks.append(bit)
        bit <<= 1 
    # create the empty bitmap
    self.map = [0]*self.nWords

  def _position(self, which) :
    # from which bit number, calculate the mask and word address
    whichBit = which % self.nBits
    self.whichWord = whichBit / self.wordSize
    self.mask      = self.masks[whichBit % self.wordSize]

  def setBit(self, which) :
    # set bit "which" to 1
    self._position(which)
    mask = self.mask
    if not self.map[self.whichWord] & mask :
      self.nSet += 1                     # count bits actually set
      self.map[self.whichWord] |= mask   # set bit to one

  def getBit(self, which) :
    # return True if bit 'which' is set, else False
    self._position(which)
    return (self.map[self.whichWord] & self.mask) != 0

def test() :
    # test code from the shell. python bitmap.py 5 16 17 5
    import sys
    tests = map(int,sys.argv[1:])
    bm = Bitmap(64)
    for t in tests :
        print "Bit",t, bm.getBit(t)
        if t >= 0 : bm.setBit(t)
        print map(hex, bm.map)
        print "  now", bm.getBit(t)

if __name__ == "__main__" : test()
