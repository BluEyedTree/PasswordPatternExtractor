def subStringFinder(word):
    count = 0
    for i in range(1,len(word)):
        for j in range(0,len (word)-i):
            wordToAdd = word[j:j+i+1]
            if (len(wordToAdd) > 2 and len(wordToAdd) < 5):
                count +=1
    print(count)


print(subStringFinder("72273"))
