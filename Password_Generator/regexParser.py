import re


def breakUPRegex(regex, breakUpNumber):
    regexlList = []
    for i in regex.split("{"):
        for j in i.split("}"):
            regexlList.append(j)

    regexlList = regexlList[:-1]

    formattedRegex = ""
    for i in range(0,len(regexlList)-1,2):
        builtRegexToAdd = regexlList[i] + "{1}"
        formattedRegex += builtRegexToAdd*int(regexlList[i+1])

    count = 0
    toAdd = []

    toBuild = ""
    for i in formattedRegex.split("{1}"): #Get the items without the number
        count += 1
        if(i != ""):
            toBuild += i+"{1}"

        if(count == breakUpNumber):
            toAdd.append(toBuild)
            toBuild = ""
            count =0

    if(toBuild != ""):
        #print(count)
        toAdd.append(toBuild)
    return toAdd
