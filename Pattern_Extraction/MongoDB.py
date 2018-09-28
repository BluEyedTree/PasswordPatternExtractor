from pymongo import MongoClient
from pymongo import UpdateOne


#collection.save({'_id' : "test", 'value' : 2})
# testing


class MongoDB():
    #A class to write data to dictionary that is stored on disk vs memory
    def __init__(self, dbFilePath):
        self.dbFilePath = dbFilePath
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['Substring_Research'] #Might have to change this back to mydb
        self.collection = self.db[dbFilePath]
        self.count =0
        self.batchList = []



    def add(self, subStringToAdd):
        self.count +=1

        if( self.count <2500000):
            self.batchList.append(UpdateOne({'_id': subStringToAdd}, {'$inc': {'value': 1}}, upsert=True))

        elif(self.count == 2500000):
            self.collection.bulk_write(self.batchList)
            self.count = 0
            self.batchList.clear()

    def close(self):
        self.collection.bulk_write(self.batchList)
        self.client.close()

