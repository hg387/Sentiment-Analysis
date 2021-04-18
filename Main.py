#!/usr/bin/python
import math, os, pickle, re
from bayes_template import *
from bayes_template_best import *


# for unigram classifier
def classify(path):
    bc = Bayes_Classifier()

    iFileList = []
    for fFileObj in os.walk(path):
        iFileList = fFileObj[2]
        break

    for filename in iFileList:
        f = open((path+filename), mode='r',encoding='utf-8')
        sTxt = f.read()
        f.close()
        result = bc.classify(sTxt) # test the sentance
        print("%s:%s" % (filename, result))

# for bigram classifer
def classify_best(path):
    bc = Bayes_Classifier_Best()

    iFileList = []
    for fFileObj in os.walk(path):
        iFileList = fFileObj[2]
        break

    for filename in iFileList:
        f = open((path+filename), mode='r',encoding='utf-8')
        sTxt = f.read()
        f.close()
        result = bc.classify(sTxt)  # test the sentance
        print("%s:%s" % (filename, result))

if __name__ == "__main__":
    testFile = "bayes.py"
    
    with open(testFile) as source_file:
	    exec(source_file.read())
    
    # Uncomment for sentance evaluation with best classifier
    # bc = Bayes_Classifier_Best()
    # result = bc.classify("60 degrees > 80 degrees")
    # print(result)

    # Uncomment for sentance evaluaton with the classifier
    # bc = Bayes_Classifier()
    # result = bc.classify("60 degrees > 80 degrees")
    # print(result)
    
    # Uncomment and put your test directory or put or test files inside movies_reviews directory
    # classify("movies_reviews/")

    classify_best("movies_reviews/")


    
    

