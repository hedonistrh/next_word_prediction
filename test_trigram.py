import pickle
from collections import OrderedDict
import heapq # for getting top elements
import time
import re


pickleDumps = "pickleDumps/"
conditionalProbabilityFileBigram = pickleDumps+"conditionalProbabilityDictBigram.p"
conditionalProbabilityFileTrigram = pickleDumps+"conditionalProbabilityDictTrigram.p"

bigramsCounterPath = pickleDumps + "bigramsCounter.p"
trigramsCounterPath = pickleDumps + "trigramsCounter.p"

file = open(conditionalProbabilityFileBigram,"rb")
conditionalProbabilityDictBigram = pickle.load(file)

file = open(conditionalProbabilityFileTrigram,"rb")
conditionalProbabilityDictTrigram = pickle.load(file)

file = open(bigramsCounterPath,"rb")
bigramsCounter = pickle.load(file)

file = open(trigramsCounterPath,"rb")
trigramsCounter = pickle.load(file)

pat = re.compile('\w+ \w+ \w+[.]*$') 

while True:

    """Just check last 2 words from input."""
    checkForThisTrigram = input("Enter a word to predict its next probable words (':)' for stopping) : ")

    if checkForThisTrigram == ":)":
        break;

    if (len(checkForThisTrigram.split(' ')) <= 2):
        print ('''Please write more than 2 words. If you just want to write 2 words,
        you can use bigram script.''')
        break


    """If user don't hit the space button at the end, 
    we need use current segment to predict next word."""

    try:
        if (len(checkForThisTrigram.split(' ')) > 3):
            i = pat.search(checkForThisTrigram)
            checkForThisTrigram = i.group()
    except AttributeError:
        pass

    """If user hit the space button at the end, we need to predict next word."""
    if (checkForThisTrigram[-1] == " "):
        checkForThisTrigram = checkForThisTrigram.split(" ")[-3] + " " + checkForThisTrigram.split(" ")[-2] + " "

    # print (checkForThisTrigram)
    start = time.time()
    # empty the list, for new iteration
    matchedBigrams = [] # all bigrams that starts with the inputted word

    for words, count in bigramsCounter.items():
        if checkForThisTrigram == words[1]:
            matchedBigrams.append(words[0]+" "+words[1])
        elif (checkForThisTrigram.split(' ')[1] == words[0]):
            length_of_second = len(checkForThisTrigram.split(' ')[2])
            if (words[1][:length_of_second] == checkForThisTrigram.split(' ')[2]):
                matchedBigrams.append(words[0]+" "+words[1])

    matchedTrigrams = [] # all trigrams that starts with the inputted word
    for words, count in trigramsCounter.items():
        if checkForThisTrigram == (words[0]+" "+words[1]):
            matchedTrigrams.append(words[0]+" "+words[1]+" "+words[2])
        elif ((checkForThisTrigram.split(' ')[0] == words[0])&
                (checkForThisTrigram.split(' ')[1] == words[1])):
            length_of_third = len(checkForThisTrigram.split(' ')[2])
            if (words[2][:length_of_third] == checkForThisTrigram.split(' ')[2]):
                matchedTrigrams.append(words[0]+" "+words[1]+" "+words[2])

    topDictBigram = {}
    for singleBigram in matchedBigrams:
        topDictBigram[singleBigram] = conditionalProbabilityDictBigram[singleBigram]

    topDictTrigram = {}
    for singleTrigram in matchedTrigrams:
        topDictTrigram[singleTrigram] = conditionalProbabilityDictTrigram[singleTrigram]
    
    topBigrams = heapq.nlargest(3, topDictBigram, key=topDictBigram.get)
    topTrigrams = heapq.nlargest(3, topDictTrigram, key=topDictTrigram.get)

    print ("\n" + "Bigrams prediction:" + "\n")
    for b in topBigrams:
        print (b +" : "+str(topDictBigram[b])+"\n")

    print ("____________________" + "\n")

    print ("Trigrams prediction:" + "\n" )
    for b in topTrigrams:
        print (b +" : "+str(topDictTrigram[b])+"\n")

    for b in topBigrams:
        pred_from_bigram = (b.split(" ")[-1])

    print ("\n" + "____________________" + "\n")
    end = time.time()
    print (end - start)