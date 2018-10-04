
'''

Input: (String) the password
Output: (List<String>) a list of substrings within the passwprd

'''
def subStringFinder(word):
    substrings = []
    for i in range(1,len(word)):
        for j in range(0,len (word)-i):
            wordToAdd = word[j:j+i+1]
            if (len(wordToAdd) > 2 and len(wordToAdd) < 9):
                substrings.append(wordToAdd)

    return substrings