#!/usr/bin/python
import math, os, pickle, re

class Bayes_Classifier:
   dictionaries = [] # object to be stored 
   results = {"negative": 0, "neutral": 0, "positive": 0}
   positiveWords = {} # positive words dictionary
   negativeWords = {} # negative words dictionary
   neutralWords = {} # neutral words dictionary not used in the calculations

   def __init__(self, trainDirectory = ("reviews" + "/")):
      '''This method initializes and trains the Naive Bayes Sentiment Classifier.  If a 
      cache of a trained classifier has been stored, it loads this cache.  Otherwise, 
      the system will proceed through training.  After running this method, the classifier 
      is ready to classify input text.'''
      obj = self.load("dictionaries")
      if obj == None:
         iFileList = []
         for fFileObj in os.walk(trainDirectory):
            iFileList = fFileObj[2]
            break

         for filename in iFileList:
            result = self.check(filename) # to check the file name
            stringWords = self.loadFile(trainDirectory + filename)
            tokenizeWords = self.tokenize(stringWords)

            if (result == "positive"):
               for i in tokenizeWords:
                  if i in self.positiveWords:
                     self.positiveWords[i] += 1
                     continue
                  self.positiveWords[i] = 1 # if not in the dictionary

            elif (result == "negative"):
               for i in tokenizeWords:
                  if i in self.negativeWords:
                     self.negativeWords[i] += 1
                     continue
                  self.negativeWords[i] = 1 # if not in the dictionary

            elif (result == "neutral"):
               for i in tokenizeWords:
                  if i in self.neutralWords:
                     self.neutralWords[i] += 1
                     continue
                  self.neutralWords[i] = 1

            self.results[result] += 1 # if not in the dictionary
         
         path = "dictionaries"
         self.dictionaries.append(self.results)
         self.dictionaries.append(self.positiveWords)
         self.dictionaries.append(self.negativeWords)
         self.dictionaries.append(self.neutralWords)

         self.save(self.dictionaries, path) # save the dictionary

      else:
         # if there is no training done before
         self.dictionaries = obj
         self.results = obj[0]
         self.positiveWords = obj[1]
         self.negativeWords = obj[2]
         self.neutralWords = obj[3]

   def train(self):   
      '''Trains the Naive Bayes Sentiment Classifier.'''
   
   def classify(self, sText):
      '''Given a target string sText, this function returns the most likely document
      class to which the target string belongs. This function should return one of three
      strings: "positive", "negative" or "neutral".
      '''
      words = self.tokenize(sText)
      P = []
      P_positive = self.smoothing_positive(words)
      P_negative = self.smoothing_negative(words)

      P_positive = (math.e ** P_positive)
      P_negative = (math.e ** P_negative)

      P.append(P_positive)
      P.append(P_negative)
      maxP = P.index((max(P)))

      if (maxP == 0):
         return "positive"
      elif (maxP ==1):
         return "negative"
      else:
         return "Not enough info"
   
   def smoothing_positive(self, words):
      # positive smoothing amoung the positive dictionary
      P_positive = math.log( ( (self.results["positive"]) / (sum(self.results.values())) ))
      for word in words:
         sum_positive_words = (sum(self.positiveWords.values()))
         if word in self.positiveWords:
            P_positive += (math.log( ( (self.positiveWords[word]) / sum_positive_words ) ))
         else:
            # 1-Smoothing
            for positiveWord in self.positiveWords:
               self.positiveWords[positiveWord] += 1
            
            self.positiveWords[word] = 1
            P_positive = self.smoothing_positive(words)
            break
      
      return P_positive
   
   def smoothing_negative(self, words):
      # negative smoothing amoung the negative dictionary
      P_negative = math.log( ( (self.results["negative"]) / (sum(self.results.values())) ))
      for word in words:
         sum_negative_words = (sum(self.negativeWords.values()))
         if word in self.negativeWords:
            P_negative += (math.log( ( (self.negativeWords[word]) / sum_negative_words ) ))
         else:
            # 1-Smoothing
            for negativeWord in self.negativeWords:
               self.negativeWords[negativeWord] += 1
            
            self.negativeWords[word] = 1
            P_negative = self.smoothing_negative(words)
            break
      
      return P_negative

   def check(self, sText):
      # To check if filename is positive or negative
      file = sText.split("-")
      if (file[1] == "1"):
        return "negative"
      elif (file[1] == "5"):
        return "positive"

      return "neutral"

   def loadFile(self, sFilename):
      '''Given a file name, return the contents of the file as a string.'''

      f = open(sFilename, mode='r',encoding='utf-8')
      sTxt = f.read()
      f.close()
      return sTxt
   
   def save(self, dObj, sFilename):
      '''Given an object and a file name, write the object to the file using pickle.'''

      f = open(sFilename, "ab+")
      p = pickle.Pickler(f)
      p.dump(dObj)
      f.close()
   
   def load(self, sFilename):
      '''Given a file name, load and return the object stored in the file.'''
      try:
         f = open(sFilename,  mode='rb')
      except FileNotFoundError:
         return None
         
      u = pickle.Unpickler(f)
      dObj = u.load()
      f.close()
      return dObj

   def tokenize(self, sText): 
      '''Given a string of text sText, returns a list of the individual tokens that 
      occur in that string (in order).'''

      lTokens = []
      sToken = ""
      for c in sText:
         if re.match("[a-zA-Z0-9]", str(c)) != None or c == "\'" or c == "_" or c == '-':
            sToken += c
         else:
            if sToken != "":
               lTokens.append(sToken)
               sToken = ""
            if c.strip() != "":
               lTokens.append(str(c.strip()))
               
      if sToken != "":
         lTokens.append(sToken)

      return lTokens
