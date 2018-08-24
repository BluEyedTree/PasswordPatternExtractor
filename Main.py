def subStringFinder(word):
    for i in range(1,len(word)):
        for j in range(0,len (word)-i):

            print(word[j:j+i+1])
