from pymongo import MongoClient
import pymongo
client = MongoClient('localhost', 27017)
#db = client["Research_Initial_Test"]
#collection = db["regex"]

db = client["Substring_Research"]
collection = db["substring_Length3and4"]

'''
#Make new item
collection.save({'_id' : "test", 'value' : 2})
# testing

#To get a single value:
oldValue = collection.find_one("test")['value']
print(oldValue)
print(collection.find_one("sdasdasd")==None)

#To update a value
collection.update_one({'_id':"test"}, {"$set": {"value": oldValue+1}}, upsert=False)

print(collection.find_one("test"))
'''

client['Research_Initial_Test']
'''
newD = {}
for obj in collection.find():
    newD[obj['_id']] = obj['value']
print(newD)
client.close()
'''
count = 0
for obj in collection.find().sort([('value', pymongo.DESCENDING)]):
    pass
    #count +=obj["value"]
    #count += 1
    print(obj)
print(count)