from pymongo import MongoClient


#collection.save({'_id' : "test", 'value' : 2})
# testing


class MongoDB():
    #A class to write data to dictionary that is stored on disk vs memory
    def __init__(self, dbFilePath):
        self.dbFilePath = dbFilePath
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['Substring_Research'] #Might have to change this back to mydb
        self.collection = self.db[dbFilePath]




    def add(self, subStringToAdd):
        strippedSubstringToAdd = subStringToAdd.rstrip()
        #if(psutil.virtual_memory().percent > 80):
         #   self.shelf.sync()

        #The case where you insert a new value
        if(self.collection.find_one(subStringToAdd) == None):
            self.collection.save({'_id': subStringToAdd, 'value': 1})
        #Case where you found the value

        else:
            oldValue = self.collection.find_one(subStringToAdd)['value']
            self.collection.update_one({'_id': subStringToAdd}, {"$set": {"value": oldValue + 1}}, upsert=False)

    def close(self):
        self.client.close()

