import re
from pymongo import MongoClient
import time
import Password_Generator.regexParser as regexParser


def combineSets(set1,set2):
    listToReturn= []
    stringToBuild =""
    for item1 in set1:
        for item2 in set2:
            listToReturn.append(item1+item2)

    return listToReturn

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
        listToReturn.append(i["_id"])


    end = time.time()
    print(end - start)
    return listToReturn


#TODO: Fill up DB with mock info and write testing code
#It was tested lightly with function below
def main():
    #TODO: Read through regex file and get regex strings

    testRegex = "[0-9]{2}[a-z]{4}"

    broken_up_regex = regexParser.breakUPRegex(testRegex,3)

    #Now lets create our sets
    setToCombine = []
    for i in broken_up_regex:
        print(i)
        setToCombine.append(createSet(i))

    firstSet = combineSets(setToCombine[0],setToCombine[1])
    setToCombine = setToCombine[2:]
    print(firstSet)
    for i in range(0,len(setToCombine)):
        firstSet = combineSets(firstSet,setToCombine[i])


        print(firstSet)


#main()


def test():
    setToCombine = []

    set1 = ["a","b","c"]
    set2 = ["1","2","3"]
    set3 = ["!","&","?"]
    set4 = ["A","B","C","D"]

    setToCombine.append(set1)
    setToCombine.append(set2)
    setToCombine.append(set3)
    setToCombine.append(set4)


    firstSet = combineSets(setToCombine[0],setToCombine[1])
    setToCombine = setToCombine[2:]
    print(firstSet)
    for i in range(0,len(setToCombine)):
        firstSet = combineSets(firstSet,setToCombine[i])

        print(firstSet)

test()