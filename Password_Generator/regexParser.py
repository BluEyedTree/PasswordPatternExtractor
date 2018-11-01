import re


testRegex = "[a-z]{3}[0-9]{3}[a-z]{4}[0-9]{3}[a-z]{3}"


def breakUPRegex_(breakUpNumber):
    regexlList = []
    for i in testRegex.split("{"):
        for j in i.split("}"):
            regexlList.append(j)

    regexlList = regexlList[:-1]
    print(regexlList)




    formattedRegex = ""
    for i in range(0,len(regexlList)-1,2):
        builtRegexToAdd = regexlList[i] + "{1}"
        formattedRegex += builtRegexToAdd*int(regexlList[i+1])

    breakUpNumber = 3
    count = 0
    toAdd = []

    toBuild = ""
    for i in formattedRegex.split("{1}"): #Get the items without the number
        count += 1
        toBuild += i+"{1}"

        if(count == breakUpNumber):
            toAdd.append(toBuild)
            toBuild = ""
            count =0

    return (toAdd)
