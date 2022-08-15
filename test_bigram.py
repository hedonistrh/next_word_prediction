import pickle
from collections import OrderedDict
import heapq # for getting top elements
import time
import re


pickleDumps = "pickleDumps/"
conditionalProbabilityFile = pickleDumps+"conditionalProbabilityDictBigram.p"
bigramsCounterPath = pickleDumps + "bigramsCounter.p"

file = open(conditionalProbabilityFile,"rb")
conditionalProbabilityDict = pickle.load(file)

file = open(bigramsCounterPath,"rb")
bigramsCounter = pickle.load(file)

pat = re.compile('\w+ \w+[.]*$') 

while True:

    """Just check last 2 words from input."""
    checkForThisBigram = input("Enter a word to predict its next probable words (':)' for stopping) : ")

    if checkForThisBigram == ":)":
        break

    """If user don't hit the space button at the end, 
    we need use current segment to predict next word."""

    try:
        if (len(checkForThisBigram.split(' ')) > 2):
            i = pat.search(checkForThisBigram)
            checkForThisBigram = i.group()
    except AttributeError:
        pass

    """If user hit the space button at the end, we need to predict next word."""
    if (checkForThisBigram[-1] == " "):
        checkForThisBigram = checkForThisBigram.split(" ")[-2]

    start = time.time()
    # empty the list, for new iteration
    matchedBigrams = [] # all bigrams that starts with the inputted word
    for words, count in bigramsCounter.items():
        if checkForThisBigram == words[0]:
            matchedBigrams.append(words[0]+" "+words[1])
        elif (checkForThisBigram.split(' ')[0] == words[0]):
            length_of_second = len(checkForThisBigram.split(' ')[1])
            if (words[1][:length_of_second] == checkForThisBigram.split(' ')[1]):
                matchedBigrams.append(words[0]+" "+words[1])

    topDict = {}
    for singleBigram in matchedBigrams:
        topDict[singleBigram] = conditionalProbabilityDict[singleBigram]

    topBigrams = heapq.nlargest(3, topDict, key=topDict.get)
    for b in topBigrams:
        print (b +" : "+str(topDict[b])+"\n")

    print ("\n" + "____________________" + "\n")
    end = time.time()
    print (end - start)