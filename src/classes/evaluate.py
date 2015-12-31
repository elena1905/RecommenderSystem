'''
Created on Mar 22, 2012

@author: Wenchong Chen

Python version 2.7

This file implements the Evaluate class.
'''

from __future__ import division, print_function
from random import random
import copy
import math
import recommender

''' A class that performs a hold-out evaluation of a recommender system'''
class Evaluate(object):
    
    '''Constructor'''
    def __init__(self,recommender):
        self.rec = recommender
        self.movies = self.rec.getMovies()
        self.results = []       # list of results [(actual, prediction)] 
        self.coverage = 0       # percentage of tests that can't be rated
        self.MSE = 0            # MSE result of test
    
    
    
    '''splitTestData() method'''
    def splitTestData(self,numTestRatings):
        ''' set up training data from ratings matrix '''
        self.training = copy.deepcopy(self.rec.getRatings())  #training ratings matrix
        self.test = []          #test data [(user, movie, rating)]
        
        ''' extract out numOfRatings ratings and save as test data, remove from ratings matrix'''
        count=0;
        while count < numTestRatings :
            #get random user and rating
            rUser = self.rec.getRandomUser()
            rMovie = self.rec.getRandomMovie()
            
            #check to see that this rating exists
            if rMovie in self.training.get(rUser):
                #set it up in test data and remove it from training data, increment count
                self.test.append((rUser, rMovie, self.training[rUser][rMovie])) 
                self.training[rUser].pop(rMovie)    #pop() removes item and returns its value
                count+=1;
    
    
    
    '''performTest() method'''
    def performTest(self):
        ''' Generate prediction for each of the tests in test data and store results '''
 
        newRec = recommender.Recommender(ratings=self.training, loadFromFiles=False)
        
        for (user, movie, rating) in self.test:
            prediction = newRec.getPrediction(user, movie)
            self.results.append((rating, prediction))
    
    
    
    '''evaluate() method'''
    def evaluate(self, percentage=.2, iterations=1):
        # return the ceiling of x as a float
        # the smallest integer value greater than or equal to x
        numTestRatings = math.ceil(self.rec.getNumRatings() * percentage)
        
        while iterations > 0:
            self.splitTestData(numTestRatings)
            self.performTest()
            iterations -= 1
        
        ''' process results - calculate MSE and numCantRate '''
        sumsq = 0.0
        numNotRated = 0.0
        for (rating, pred) in self.results:
            if pred == -1:
                numNotRated += 1;
            else :
                sumsq += math.pow((rating-pred),2)
        
        # number of rated items
        numRated = len(self.results) - numNotRated
        
        # calculate coverage and Mean Squared Error
        self.coverage = numRated / len(self.results)
        self.MSE = sumsq / numRated
    
    
    
    '''getMSE() method'''
    def getMSE(self):
        return self.MSE
    
    
    
    '''getCoverage() method'''
    def getCoverage(self):
        return self.coverage
    
    
    
    ''' ******* The End ****** '''