'''
Created on Feb 22, 2012

@author: Wenchong Chen

Python version 2.7

This file implements six similarity functions:
1. mean squared difference similarity function
2. pearson's correlation coefficient similarity function
3. cosine similarity function
4. spearman rank correlation similarity function
5. spearman rank correlation using Michiel de Hoon's library
6. spearman rank correlation using another formula
'''

import math
import scipy.stats.stats
import Bio.Cluster

'''1: mean squared difference similarity function'''
def weighted_similarity1(ratings, person1, person2):
    num_corated_item = 0
    sum_of_squares = 0
    
    for item in ratings[person1]:
        if item in ratings[person2]:
            # count number of corated items
            num_corated_item += 1
            
            # sum up sum of squares
            sum_of_squares += pow(ratings[person1][item] - ratings[person2][item], 2)
    
    # if they are no ratings in common, return -1
    if num_corated_item == 0:
        return -1
    
    # make sure difference is not divided by zero
    #if number_of_corated_item != 0:
    
    # calculate the difference
    difference = sum_of_squares / num_corated_item
        
    # calculate the similarity
    similarity = 1 - difference / 16
    
    return similarity



'''2: pearson's correlation coefficient similarity function'''
def weighted_similarity(ratings, person1, person2):
    ''' Pearson's Correlation Coefficient'''
    ''' improved similarity assessment'''
    
    # Get the list of mutually rated items
    si=[]
    for item in ratings[person1]:
        if item in ratings[person2]:
            si.append(item)
    
    # if they are no ratings in common, return -1
    if len(si) == 0:
        return -1
    
    # calculate average ratings for person1 & person2
    avg1 = sum([ratings[person1][item] for item in ratings[person1]]) / len(ratings[person1])
    avg2 = sum([ratings[person2][item] for item in ratings[person2]]) / len(ratings[person2])
    
    # initialise accumulators
    num = 0
    sumSq1 = 0
    sumSq2 = 0
    
    for item in si:
        # Accumulate the numerator
        d1 = ratings[person1][item] - avg1
        d2 = ratings[person2][item] - avg2
        num += d1 * d2
        
        # accumulate the sum of sqrs
        sumSq1 += pow(d1,2)
        sumSq2 += pow(d2,2)
    
    # Calculate pearson score
    den = math.sqrt(sumSq1 * sumSq2)
    if den == 0:
        return 0
    
    similarity = num / den
    
    return similarity



'''3: cosine similarity function'''
def weighted_similarity3(ratings, person1, person2):
    
    # Get the list of mutually rated items
    si=[]
    for item in ratings[person1]:
        if item in ratings[person2]:
            si.append(item)
    
    # if they are no ratings in common, return -1
    if len(si) == 0:
        return -1
    
    # initialise accumulators
    num = 0
    sumSq1 = 0
    sumSq2 = 0
    
    for item in si:
        # Accumulate the numerator
        r1 = ratings[person1][item]     # rating(ui, itemk)
        r2 = ratings[person2][item]     # rating(uj, itemk)
        num += r1 * r2
        
        # accumulate the sum of sqrs
        sumSq1 += pow(r1,2)
        sumSq2 += pow(r2,2)
    
    # Calculate cosine score
    den = math.sqrt(sumSq1 * sumSq2)
    if den == 0:
        return 0
    
    similarity = num / den
    
    return similarity



'''4: spearman rank correlation similarity function'''
def weighted_similarity4(ratings, person1, person2):
    ''' Spearman's Rank Correlation Coefficient'''
    ''' improved similarity assessment'''
    
    # n is the number of corated items
    n = 0
    rating1 = []
    rating2 = []
    
    # Get the ratings of corated items for person1 and person 2
    for item in ratings[person1]:
        if item in ratings[person2]:
            rating1.append(ratings[person1][item])
            rating2.append(ratings[person2][item])
            n += 1
    
    # if they are no ratings in common, return -1
    if len(rating1) == 0:
        return -1
    
    # get the rakings for person1 and person2
    ranking1 = scipy.stats.stats.rankdata(rating1)
    ranking2 = scipy.stats.stats.rankdata(rating2)
    
    # initialize the rakings dictionaries of corated items for person1 and person 2
    R1 = {}
    R2 = {}
    for item in ratings[person1]:
        if item in ratings[person2]:
            R1[item] = 0.0
            R2[item] = 0.0
    
    # get the rakings dictionaries of corated items for person1 and person 2
    i = 0
    for item in R1:
        R1[item] = ranking1[i]
        R2[item] = ranking2[i]
        i += 1
    
    # calculate the substrahend
    sub = n * pow(((n + 1) / 2), 2)
    
    # calculate every intermediate values for calculating rho
    product = 0
    square1 = 0
    square2 = 0
    for item in R1:
        product += R1[item] * R2[item]
        square1 += pow(R1[item], 2)
        square2 += pow(R2[item], 2)
    diff3 = product - sub
    diff1 = square1 - sub
    diff2 = square2 - sub
    
    den = math.sqrt(diff1 * diff2)
    if den == 0:
        return 0
    
    # calculate rho
    similarity = diff3 / den
    
    return similarity



'''5: spearman rank correlation using Michiel de Hoon's library'''
def weighted_similarity5(ratings, person1, person2):
    ''' Spearman's Rank Correlation Coefficient'''
    ''' improved similarity assessment'''
    
    # Get the ratings of corated items for person1 and person 2
    rating1 = []
    rating2 = []
    for item in ratings[person1]:
        if item in ratings[person2]:
            rating1.append(ratings[person1][item])
            rating2.append(ratings[person2][item])
    
    # if they are no ratings in common, return -1
    if len(rating1) == 0:
        return -1
    
    # calculate spearman's similarity using Michiel de Hoon's library
    # dist='s' means spearman
    similarity = 1 - Bio.Cluster.distancematrix((rating1, rating2), dist='s')[1][0]
    
    return similarity



'''6: spearman rank correlation using another formula'''
def weighted_similarity6(ratings, person1, person2):
    ''' Spearman's Rank Correlation Coefficient'''
    ''' improved similarity assessment'''
    
    # n is the number of corated items
    n = 0
    rating1 = []
    rating2 = []
    
    # Get the ratings of corated items for person1 and person 2
    for item in ratings[person1]:
        if item in ratings[person2]:
            rating1.append(ratings[person1][item])
            rating2.append(ratings[person2][item])
            n += 1
    
    # if they are no ratings in common, return -1
    if len(rating1) == 0:
        return -1
    
    # get the rakings for person1 and person2
    ranking1 = scipy.stats.stats.rankdata(rating1)
    ranking2 = scipy.stats.stats.rankdata(rating2)
    
    # initialize the rakings dictionaries of corated items for person1 and person 2
    R1 = {}
    R2 = {}
    for item in ratings[person1]:
        if item in ratings[person2]:
            R1[item] = 0.0
            R2[item] = 0.0
    
    # get the rakings dictionaries of corated items for person1 and person 2
    i = 0
    for item in R1:
        R1[item] = ranking1[i]
        R2[item] = ranking2[i]
        i += 1
    
    # calculate average rankings for person1 & person2
    avg1 = sum([item for item in ranking1]) / n
    avg2 = sum([item for item in ranking2]) / n
    
    # calculate every intermediate values for calculating rho
    diff1 = 0
    diff2 = 0
    sum1 = 0
    sum2 = 0
    product = 0
    for item in R1:
        diff1 = R1[item] - avg1
        diff2 = R2[item] - avg2
        
        product += diff1 * diff2
        sum1 += pow(diff1, 2)
        sum2 += pow(diff2, 2)
    
    den = math.sqrt(sum1 * sum2)
    if den == 0:
        return 0
    
    # calculate rho
    similarity = product / den
    
    return similarity



''' ******* The End ****** '''