import DiskDic
import shelve
import re


dictionary= DiskDic.DiskDic("substring")
dictionary_regex = DiskDic.DiskDic("regex")

def subStringFinder(word):
    for i in range(1,len(word)):
        for j in range(0,len (word)-i):
            wordToAdd = word[j:j+i+1]
            if (len(wordToAdd) < 8): #Only words under 7 chars will be added
                dictionary.add(wordToAdd)


def regexFinder(word):
    regexList = []
    with open("/Users/thomasbekman/Documents/Research/Regex_toFormat.txt") as f:
        for line in f:
            formattedLine = "^" + line[:-1] + "$"  # The [:-1] is to deal with new lin charecters

            if (line.find("\n") == -1):
                formattedLine = "^" + line + "$"
            regexList.append(formattedLine)


    for regex in regexList:
        # print("Im the Rgex:   "+ regex)
        if (re.match(regex, str(word)) is not None):
            dictionary_regex.add(regex)
            break



def main(filePath):
    iter_count = 0
    rockYouLength = 24342374
    with open(filePath) as infile:
        for line in infile:
            iter_count += 1
            if (iter_count % 1000 == 0):
                print(str(iter_count / rockYouLength * 100) + str("% Done"))
            subStringFinder(line)
            regexFinder(line)

    dictionary.close()
    dictionary_regex

main("/Users/thomasbekman/Documents/Research/Passwords/Cracked_Passwords/totalList.txt")



