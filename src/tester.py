'''
Created on Feb 22, 2012

@author: Wenchong Chen

Python version 2.7

This tester is for testing the recommender
and the evaluate systems.
'''

import classes.recommender
import classes.evaluate


# initialise ratings and movies file paths
ratingsFile = "../data/ratings.dat"
moviesFile = "../data/movies.dat"
# initialise testdata path
testFile = "../data/testdata.dat"
# initialise predictions file path to store predictions
predictionsFile = '../data/predictions.dat'

# instanciate Recommender class
myRecommender = classes.recommender.Recommender(ratingsFile, moviesFile)

# store prediction results into predictions*.dat
#myRecommender.testFromFile(predictionsFile, testFile)

# instanciate Evaluate class
myEvaluate = classes.evaluate.Evaluate(myRecommender)
myEvaluate.evaluate(percentage=.01)
#myEvaluate.evaluate(percentage=.01, iterations=10)

mse = myEvaluate.getMSE()
coverage = myEvaluate.getCoverage()

print ("mse: ", mse)
print ("coverage: ", coverage)

# print blank line
print

'''**** Test Area Below ****'''

# test number of ratings for person1
#rate = myRecommender.ratings['344']
#num = len(rate)
#print num

# test testFromFile
#myRecommender.testFromFile(testFile)

# test getRecommendations()
#rec = myRecommender.getRecommendations('514')
#print "recommendation: ", rec

# test getPrediction()
#userId = myRecommender.getRandomUser()
#movieName = myRecommender.getRandomMovie()
#pred = myRecommender.getPrediction('514', 'Donnie Brasco (1997)')
#print "prediction: ", pred

# test getNumUsers()
#print "number of users: ", myRecommender.getNumUsers()

# test getNumMovies()
#print "number of movies: ", myRecommender.getNumMovies()

# test getNumRatings()
#print "number of ratings: ", myRecommender.getNumRatings()

# test recommender.py
#print "movies dictionary: ", myRecommender.movies



''' ******** The End *******'''