'''
Created on Feb 22, 2012

@author: Wenchong Chen

Python version 2.7

This file implements the Recomender class.
'''

from __future__ import print_function
import math
import random
import functions.similarity



''' A class that sets up the ratings matrix '''
class Recommender(object):
    
    '''constructor'''
    def __init__(self, ratingsFile=None, moviesFile=None,loadFromFiles=True, ratings={}):
        ''' define ratings dict and movies dict'''
        ''' loadData() loads data from two files and initialise the two dicts'''
        self.ratings = {}
        self.movies = {}
        if loadFromFiles:
            self.loadData(ratingsFile, moviesFile)
        else :
            self.ratings = ratings
    
    
    
    '''loadData() method'''
    def loadData(self, ratingsFile, moviesFile):
        ''' load data from movie and users' rating files'''
        ''' store data in movies and ratings dicts'''
        # keep the dictionary structure in mind
        ''' load movies'''
        for line in open(moviesFile):
            movieList = line.split('|')
            movieid = movieList[0]
            moviename = movieList[1]
            # both of the following do the same thing
            #self.movies.setdefault(movieid, moviename)
            self.movies[movieid] = moviename
        ''' load ratings'''
        for line in open(ratingsFile):
            (user, movieid, rating, timestamp) = line.split('\t')
            self.ratings.setdefault(user, {})
            self.ratings[user][self.movies.get(movieid)] = float(rating)
    
    
    
    ''' getNeighbourhood() method: Fixed Size'''
    def getNeighbourhood(self, person, similarity, n=200):
        ''' returns the best matches for person from the ratings dictionary as a list'''
        ''' Number of results is optional params'''
        
        # return a similarity score list with person that looks like
        # scores = [(3.0, 'Mary'), (4.2, 'Tim'), ...] with person
        # similarity function is called here
        scores = [(similarity(self.ratings, person, other), other) 
                  for other in self.ratings if other != person]
        
        # remove any negative similarity scores --> no correlation with user so don't use them
        bestMatches = [(sim, user)
                       for (sim, user) in scores if sim>0]
        
        # rank numbers from low to high
        bestMatches.sort()
        # reverse ranking (result: high to low)
        bestMatches.reverse()
        
        # return first n highest numbers as a list
        return bestMatches[0:n]
    
    
    
    '''getRecommendations() method'''
    def getRecommendations(self, person, similarity=functions.similarity.weighted_similarity):
        ''' gets recommendations for a person by using a weighted average of neighbourhood ratings'''

        totals={}         #dict to hold item and numerator
        simSums={}        #dict to hold item and denominator
        ratingCount={}    #dict to hold item and rating count
        
        # similarity function is called inside getNeighbourhood() method
        bestMatches = self.getNeighbourhood(person, similarity)
        
        # for sim, other in bestMatches: --> why this works?
        for (sim, other) in bestMatches:
            
            for item in self.ratings[other]:
                
                # only predict for items person hasn't seen yet
                if item not in self.ratings[person] or self.ratings[person][item] == 0:

                    #count up number of ratings for this item
                    ratingCount.setdefault(item, 0)
                    ratingCount[item] += 1

                    # Similarity * Score - accumulate into numerator
                    totals.setdefault(item,0)
                    totals[item] += self.ratings[other][item] * sim

                    # Sum of similarities - accumulate into denominator
                    simSums.setdefault(item,0)
                    simSums[item] += math.fabs(sim)

        predictions = []
        # Create the list of predictions for new items
        for item, total in totals.items():
            predictions.append((total/simSums[item], item))
        
        # Return the sorted list
        predictions.sort()
        predictions.reverse()
        
        return predictions
    
    
    
    '''1: getPrediction() method: simple prediction approach'''
    def getPrediction1(self, person, item, similarity=functions.similarity.weighted_similarity):
        ''' get single prediction for given person and item, returns -1'''
        ''' if it cannot perform the prediction either as'''
        ''' the person has already rated the item'''
        ''' or there are not adequate ratings in matrix'''
        
        total = 0
        simSum = 0
        ratingCount = 0
        
        #check item not already rated by person - if so return -1
        if item in self.ratings.get(person):
            return -1
        
        # get neighbourhood
        # similarity function is called inside getNeighbourhood() method
        bestMatches = self.getNeighbourhood(person, similarity, n = 300)
        
        for sim, other in bestMatches:
            if item in self.ratings[other]:
                # count up num of ratings for this item
                ratingCount += 1
                
                # similarity(ui, uj) * rating(uj, item) - accumulate into numerator
                total += self.ratings[other][item] * sim
                
                # sum of similarities - accumulate into denominator
                simSum += sim
                
        # calculate predictions for item, make sure there was at least 1 rating
        if ratingCount != 0:
            prediction = total / simSum
        else:
            prediction = -1
                
        return prediction
    
    
    
    '''2: getPrediction() method: Resnick's Formula - improved prediction approach'''
    def getPrediction(self, person, item, similarity=functions.similarity.weighted_similarity):
        ''' get single prediction for given person and item, returns -1'''
        ''' if it cannot perform the prediction either as'''
        ''' the person has already rated the item'''
        ''' or there are not adequate ratings in matrix'''
        
        total = 0
        simSum = 0
        ratingCount = 0
        
        # check item not already rated by person - if so return -1
        if item in self.ratings.get(person):
            return -1
        
        # calculate average rating for person: active user
        ''' do not use item because it is a parameter passed in '''
        ''' use all_item instead '''
        avgRating1 = sum([self.ratings[person][all_item] for all_item in self.ratings[person]]) / len(self.ratings[person])
        
        # get neighbourhood
        # similarity function is called inside getNeighbourhood() method
        bestMatches = self.getNeighbourhood(person, similarity, n = 300)
        
        for sim, other in bestMatches:
            #calculate average rating for user j
            ''' do not use item because it is a parameter passed in '''
            ''' use all_item instead '''
            avgRating2 = sum([self.ratings[other][all_item] for all_item in self.ratings[other]]) / len(self.ratings[other])
            
            if item in self.ratings[other]:
                # count up num of ratings for this item
                ratingCount += 1
                
                # similarity * (rating - avgRating2) - accumulate into numerator
                total += (self.ratings[other][item] - avgRating2) * sim
                
                # sum of similarities - accumulate into denominator
                simSum += sim
                
        # calculate predictions for item, make sure there was at least 1 rating
        if ratingCount != 0:
            prediction = avgRating1 + total / simSum
        else:
            prediction = -1
                
        return prediction
    
    
    
    '''testFromFile() method'''
    def testFromFile(self, predictionsFile, filename):
        ''' generates predictions for a group of (user, movie) pairs read in from a file'''
        ''' outputs the predictions to a file'''
        
        outfile = open(predictionsFile, 'w')
        
        # read each line from file
        for line in open(filename):
            # extract user and movie and get prediction
            (user, movie) = line.strip().split("\t")
            #(user, movie) = line.split("\t")
            pred = self.getPrediction(user, movie)
            
            # format a string for output and write to file
            tempstr = user + "\t" + movie + "\t" + str(pred)
            print(tempstr, file = outfile)
        
        outfile.close()
    
    
    
    '''getRatings() method'''
    def getRatings(self):
        return self.ratings
    
    
    
    '''getMovies() method'''
    def getMovies(self):
        return self.movies
    
    
    
    '''getRandomUser() method'''
    def getRandomUser(self):
        userId = str(random.randint(1, len(self.ratings)))
        return userId
    
    
    
    '''getRandomMovie() methos'''
    def getRandomMovie(self):
        movieId = str(random.randint(1, len(self.movies)))
        movieName = self.movies.get(movieId)
        return movieName
    
    
    
    '''getSimilarity() method'''
    def getSimilarity(self, userId, testUser):
        similarity = functions.similarity.weighted_similarity(self.ratings, userId, testUser)
        return similarity
    
    
    
    '''getNumUsers() method'''
    def getNumUsers(self):
        # a user may appear more than once, why is it counted only once?
        return len(self.ratings)
    
    
    
    '''getNumRatings() method'''
    def getNumRatings(self):
        count = 0
        # in this case, item is a dictionary: movies={movieid:moviename}
        for item in self.ratings.values():
            count += len(item)
        return count
    
    
    
    '''getNumMovies() method'''
    def getNumMovies(self):
        return len(self.movies)
    
    
    
    ''' ******* The End ****** '''