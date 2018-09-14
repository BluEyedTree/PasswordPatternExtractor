import shelve


'''
This file goes through you hashmaps on disk, sorts tyhe results and prints them out

'''

a =[]
with shelve.open('regex', 'r') as shelf:
    for key in shelf.keys():
        #print(key+" "+ str(shelf[key]))
        a.append((shelf[key],key))
    a.sort(reverse=True)

for item in a:
    print(item)



print("-----------------")
a =[]
with shelve.open('substring', 'r') as shelf:
    for key in shelf.keys():
        #print(key+" "+ str(shelf[key]))
        a.append((shelf[key],key))
    a.sort(reverse=True)

for item in a:
    print(item)



