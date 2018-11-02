import re
from pymongo import MongoClient
import time




def createSet(regex):
    start = time.time()
    regx = re.compile("^" + regex+ "$")
    listToReturn = []


    # MongoDB information
    SUBSTRING_DATABASE = "Substring_Research"
    SUBSTRING_COLECTION = "substring_Length3to8"


    # MongoDB objects
    client = MongoClient('localhost', 27017)


    db = client[SUBSTRING_DATABASE]
    collection = db[SUBSTRING_COLECTION]

    for i in  collection.find({"_id":regx}):
        listToReturn.append(i)


    end = time.time()
    print(end - start)
    return listToReturn

createSet("[a-z]{5}")