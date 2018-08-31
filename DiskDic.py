import shelve
import psutil



class DiskDic():
    #A class to write data to dictionary that is stored on disk vs memory
    def __init__(self, dbFilePath):
        self.dbFilePath = dbFilePath
        self.dbFilePath = dbFilePath
        self.shelf = shelve.open(self.dbFilePath,'n',writeback=True)

    def add(self, subStringToAdd):
        strippedSubstringToAdd = subStringToAdd.rstrip()
        if(psutil.virtual_memory().percent > 80):
            self.shelf.sync()


        try:
            oldValue = self.shelf[strippedSubstringToAdd]
            self.shelf[strippedSubstringToAdd] = oldValue+1


        except KeyError:
            self.shelf[strippedSubstringToAdd] = 1

    def close(self):
        self.shelf.close()

