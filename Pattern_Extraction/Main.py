from MongoDB import MongoDB
import re


#dictionary_regex = MongoDB("regex")
dictionary= MongoDB("substring_Length3to8")



def subStringFinder(word):
    for i in range(1,len(word)):
        for j in range(0,len (word)-i):
            wordToAdd = word[j:j+i+1]
            if (len(wordToAdd) > 2 and len(wordToAdd) < 9):
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
    rockYouLength = 23368679
    print(filePath)
    with open(filePath, encoding="utf-8") as infile:
        for line in infile:
            #print(line)
            iter_count += 1
            if (iter_count % 100 == 0):
                print(str(iter_count / rockYouLength * 100) + str("% Done"))
            line = line.rstrip("\n")
            subStringFinder(line)
            #regexFinder(line)

    dictionary.close()
    #dictionary_regex.close()

main("/Users/thomasbekman/Documents/Research/Passwords/Cracked_Passwords/UTF8_Formatted.txt")



