import pymongo
from pymongo import MongoClient
from pymongo import InsertOne, DeleteMany, ReplaceOne, UpdateOne
'''
rules_to_write = []
with open("/Users/thomasbekman/Documents/Research/SpadeFiles/MinSup20000,MinConf0.1_HalfData/Patterns_halfData.txt", encoding="utf-8") as f:
    for line in f:
        association_rule =line.split(",")[0]
        confidence = line.split(",")[1].rstrip("\n")
        print(association_rule)
        print(confidence)
        rules_to_write.append((association_rule,confidence))


client = MongoClient('localhost', 27017)
db = client['Association_Rules'] #Might have to change this back to mydb
collection = db["Association_Rules_half_data_0.1_Confidence"]

batch_to_write = []


for item in rules_to_write:
    batch_to_write.append(InsertOne({'_id': item[0], 'value': item[1]}))

collection.bulk_write(batch_to_write)
'''

client = MongoClient('localhost', 27017)
db = client['Association_Rules'] #Might have to change this back to mydb
collection = db["Association_Rules_half_data_0.1_Confidence"]

#To print out values in order.
for obj in collection.find().sort([('value', pymongo.DESCENDING)]):
    pass
    #count +=obj["value"]
    #count += 1
    print(obj)
xz
for obj in collection.find():

    #count +=obj["value"]
    #count += 1
    print(obj)
