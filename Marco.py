class Lz77:
    def init (self, inputStr):
        self.inputStr = inputStr #input stream
        self.searchSize = 5 #Search buffer (coded area) size
        self.aheadSize = 3 #lookAhead buffer (area to be encoded) size
        self.windSpiltIndex = 0 #lookHead index of buffer start
        self.move = 0
        self.notFind = -1 #No matching string found

    #Get the end index of the sliding window
    def getWinEndIndex (self):
        return self.windSpiltIndex + self.aheadSize

    #Get the start index of the sliding window
    def getWinStartIndex (self):
        return self.windSpiltIndex-self.searchSize

    #Determine if the lookHead buffer is empty
    def isLookHeadEmpty (self):
        return True if self.windSpiltIndex + self.move> len (self.inputStr)-1 else False

    def encoding (self):
        step = 0
        print ("Step Position Match Output")
        while not self.isLookHeadEmpty ():
            # 1. Sliding window
            self.winMove ()
            # 2. Get the offset and length of the largest matching string
            (offset, matchLen) = self.findMaxMatch ()
            # 3. Set the distance the window needs to slide next
            self.setMoveSteps (matchLen)
            if matchLen == 0:
                #Match is 0, indicating no string match, output the next letter to be encoded
                nextChar = self.inputStr [self.windSpiltIndex]
                result = (step, self.windSpiltIndex, '-', '(0,0)' + nextChar)
            else:
                result = (step, self.windSpiltIndex, self.inputStr [self.windSpiltIndex-offset: self.windSpiltIndex-offset + matchLen], '(' + str (offset) + ',' + str (matchLen) + ')')
            # 4. Output results
            self.output (result)
            step = step + 1 #Used only to set the step

    #Sliding window (moving demarcation point)
    def winMove (self):
        self.windSpiltIndex = self.windSpiltIndex + self.move

    #Find the maximum matching character and return the offset value and matching length from the window demarcation point
    def findMaxMatch (self):
        matchLen = 0
        offset = 0
        minEdge = self.minEdge () + 1 #Get the right edge of the coding area
        #Iterate through the area to be encoded and find the maximum matching string
        for i in range (self.windSpiltIndex + 1, minEdge):
            #print ("i:% d"% i)
            offsetTemp = self.searchBufferOffest (i)
            if offsetTemp == self.notFind:
                return (offset, matchLen)
            offset = offsetTemp #offset value

            matchLen = matchLen + 1 # Every time a match is found, add 1

        return (offset, matchLen)

    #Input parameter string exists in the search buffer, if it exists, returns the starting index of the matching string
    def searchBufferOffest (self, i):
        searchStart = self.getWinStartIndex ()
        searchEnd = self.windSpiltIndex
        #The following ifs are special cases at the beginning of processing
        if searchEnd <1:
            return self.notFind
        if searchStart <0:
            searchStart = 0
            if searchEnd == 0:
                searchEnd = 1
        searchStr = self.inputStr [searchStart: searchEnd] #Search area string
        findIndex = searchStr.find (self.inputStr [self.windSpiltIndex: i])
        if findIndex == -1:
            return -1
        return len (searchStr)-findIndex

    #Set the number of steps to slide in the next window
    def setMoveSteps (self, matchLen):
        if matchLen == 0:
            self.move = 1
        else:
            self.move = matchLen

    def minEdge (self):
        return len (self.inputStr) if len (self.inputStr)-1 <self.getWinEndIndex () else self.getWinEndIndex () + 1

    def output (self, touple):
        print ("% d% d% s% s"% touple)

if name == "main":
    lz77 = Lz77 ("AABCBBABC")
    lz77.encoding () 