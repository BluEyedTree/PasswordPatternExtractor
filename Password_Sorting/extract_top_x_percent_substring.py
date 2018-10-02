from pymongo import MongoClient
import pickle

'''
The first step is to read through the mongoDB, and dump all the values into a list. This list is then pickled.
This list will be sorted and used to create the X percentile cutoff
'''
def createValueListpickle()

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
Using the pickled value list determine the value at which to cutoff
'''
def determinePercentageCutoff(percentile_cutoff):
    f = open('valueList.pkl', 'rb')   # 'r' for reading; can be omitted
    value_list = pickle.load(f)         # load file content as mydict
    f.close()


    count = 0
    for item in value_list:
        if item>1:
            count +=1
    print(count)
    print(len(value_list))
    print("----------")
    print(value_list[24127483])
    print("----------")
    print(value_list[24127482])
    print("---------------")

    print(value_list[0])
