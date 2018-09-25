import shelve
import dbm

'''
#To play with dbm based shelf
db = dbm.open('test_dbm', 'n')
#db_sub = dbm.open('substring_dbm', 'n')
play = shelve.Shelf(db)

play["test"] = 1
play["clost"] = 2
print(play["test"])
print(play["clost"])
db.close()
'''


'''
This file goes through you hashmaps on disk, sorts tyhe results and prints them out. A pretty printer

'''

a =[]
with shelve.open('substring_dbm', 'r') as shelf:
    for key in shelf.keys():
        print(key+" "+ str(shelf[key]))
        #a.append((shelf[key],key))
    a.sort(reverse=True)

for item in a:
    print(item)

'''

print("-----------------")
a =[]
with shelve.open('substring', 'r') as shelf:
    for key in shelf.keys():
        #print(key+" "+ str(shelf[key]))
        a.append((shelf[key],key))
    a.sort(reverse=True)

for item in a:
    print(item)

'''
#print(whichdb.whichdb('test.db'))
