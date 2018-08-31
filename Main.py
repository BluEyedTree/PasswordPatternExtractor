import DiskDic
import shelve
import LetterSorter
dictionary= DiskDic.DiskDic("substring")

def subStringFinder(word):
    for i in range(1,len(word)):
        for j in range(0,len (word)-i):
            wordToAdd = word[j:j+i+1]
            if (len(wordToAdd) < 8): #Only words under 7 chars will be added
                dictionary.add(wordToAdd)




def main(filePath):
    with open(filePath) as infile:
        for line in infile:
            subStringFinder(line)

    dictionary.close()

main("/Users/thomasbekman/Documents/Passwords/Cracked_Passwords/myspace_real.txt")


#Code to test sorting. TODO: Add to test files

shelf = shelve.open("substring")
a = []
for key in shelf.keys():
    print(key+" "+ str(shelf[key]))
    a.append((shelf[key],key))
a.sort()

for item in a:
    print(item)
