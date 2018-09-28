from pymongo import MongoClient
import pymongo
client = MongoClient('localhost', 27017)
#db = client["Research_Initial_Test"]
#collection = db["regex"]

db = client["test"]
collection = db["test"]

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
#This line is what does the updating. This single line will place new values in if they don't exist, and update ones that do
#UpdateOne({'_id': "bam"}, {'$inc': {'value': 1}}, upsert=True)




#collection.update_one({'_id': "bam"}, {'$inc': {'value': 1}}, upsert=True)
count = 0
meh = []
for obj in collection.find().sort([('value', pymongo.DESCENDING)]):
    #pass
    #count +=obj["value"]
    #count += 1
    #collection.update_one({'_id': 4}, {'$inc': {'j': 1}}, upsert=True)
    meh.append(obj)
    print(obj)

print(meh[1:100])

print(count)

