from pymongo import MongoClient
import pickle
import math
import numpy
import os
from pymongo import MongoClient
import pymongo

#TODO: Create pickling file for the associations DB. Then create a cutoff function

'''
The first step is to read through the mongoDB, and dump all the values into a list. This list is then pickled.
This list will be sorted and used to create the X percentile cutoff
SUBSTRING DATA
'''
def createValueListpickle():

    client = MongoClient('localhost', 27017)
    db = client["Substring_Research"]
    collection = db["substring_Length3to8"]

    value_list = []

    for obj in collection.find():
        print(obj)
        value_list.append(obj["value"])
    print("Sort start")
    value_list.sort(reverse=True)
    print("Sort done")




    print("Pickle Start")
    f = open('valueList.pkl', 'wb')   # Pickle file is newly created where foo1.py is         # dump data to f
    pickle.dump(value_list,f)
    f.close()

'''
Using the pickled value list determine the value at which to cutoff.
The cutoff is determined as follows.
You find the index of the last two in the array.
Then 20% of the length of this is used.
~65% of the data is substrings that occur once. 
This method returns the value at the 20% percentile index
'''

def determinePercentageCutoff(percentile_cutoff):
    #Create the pickle file if it doesn't exist
    if (not os.path.isfile('valueList.pkl')):
        createValueListpickle()

    f = open('valueList.pkl', 'rb')  # 'r' for reading; can be omitted
    value_list = pickle.load(f)  # load file content as mydict
    f.close()

    count = 0
    for i in value_list:
        count +=1
        if i==1:
            first2Value = count-2
            return value_list[round(first2Value*percentile_cutoff)]




def determinePercentageCutoff_For_Regex(percentile_cutoff):
    REGEX_DATABASE = "Research_Initial_Test"
    REGEX_COLLECTION = "regex"
    client = MongoClient('localhost', 27017)

    regex_list = []
    db = client[REGEX_DATABASE]
    collection = db[REGEX_COLLECTION]
    for obj in collection.find().sort([('value', pymongo.DESCENDING)]):
        # print(obj)
        regex_list.append(obj)
    a = regex_list[math.floor(len(regex_list)*percentile_cutoff)]
    return regex_list[math.floor(len(regex_list)*percentile_cutoff)]['value']



#print(determinePercentageCutoff(0.01))




