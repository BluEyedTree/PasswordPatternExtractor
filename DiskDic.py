import shelve






class DiskDic():
    #A class to write data to dictionary that is stored on disk vs memory
    def __init__(self, dbFilePath):
        self.dbFilePath = "substring.db"
        self.dbFilePath = dbFilePath

    def add(self, subStringToAdd):
        with shelve.open(self.dbFilePath, 'c') as shelf:
            try:
                shelf[subStringToAdd] += 1
            except KeyError:
                shelf[subStringToAdd] = 1


'''
Below is an example of how to make a dbm with python
'''


'''
with shelve.open('substring', 'c') as shelf:
    shelf['ints'] = 2


with shelve.open('substring', 'c') as shelf:
    shelf['meh'] = 1

with shelve.open('substring', 'c')  as shelf:
    print(shelf["meh"])
    print(shelf["ints"])
    try:
        print(shelf["sdas"]) #TODO Use try catch to deal with the case where an entry doesn't already exist
    except KeyError:
        shelf["sdas"]=1
'''