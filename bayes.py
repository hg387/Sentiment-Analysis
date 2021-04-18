#!/usr/bin/python
import math, os, pickle, re
from bayes_template import *
from bayes_template_best import *

def bayes():
    Bayes_Classifier("reviews" + "/") # edit out the path to change the training directory
    

def bayes_best():
    Bayes_Classifier_Best("reviews" + "/") # edit out the path to change the training directory
    

if __name__ == "__main__":
    # to initialize the classifer to train 
    bayes() # for simple classifier
    bayes_best() # for best classifier