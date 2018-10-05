from pymongo import MongoClient
import pickle
import math
import numpy

'''
The first step is to read through the mongoDB, and dump all the values into a list. This list is then pickled.
This list will be sorted and used to create the X percentile cutoff
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
The length of the substring list (containing all substrings) list is determined.
THe cutoff is after 20% of the data (based on the length of the array]
So if you had the array:
[10,9,8,7,6,5,4,3,2,1]
The cutoff would be 9. Thus values would need to be greater 9 to meet it
'''
def determinePercentageCutoff(percentile_cutoff):
    f = open('valueList.pkl', 'rb')   # 'r' for reading; can be omitted
    value_list = pickle.load(f)         # load file content as mydict
    f.close()

    cutOff = value_list[round(len(value_list) * percentile_cutoff)]

    return cutOff


#print(determinePercentageCutoff(0.2))