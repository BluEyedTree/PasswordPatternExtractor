import re

#To get exact regex match wrap the regex in ^ and $



#Function to read through regex file, and format it correctly (with prepending ^ and appending $, for exact matching
regexList = []
with open ("/Users/thomasbekman/Documents/Research/Regex_toFormat.txt") as f:
    for line in f:
        formattedLine = "^" + line[:-1] + "$" #The [:-1] is to deal with new lin charecters


        if (line.find("\n") == -1):
            formattedLine = "^"  + line + "$"
        regexList.append(formattedLine)

print(regexList)
'''
print(re.match("^[A-Za-z0-9]{2}$", "a1", flags=0))


regexList = ["^[0-9]{2}$","^[A-Z]{2}$","^[a-z]{1}[0-9]{1}$","^[A-Z]{1}[a-z]{1}$","^[A-Za-z0-9]{2}$","^[A-Z]{1}[0-9]{1}$","^[a-z]{1}[A-Za-z0-9]{1}$","^[A-Za-z0-9]{1}[0-9]{1}$","^[0-9]{1}[a-z]{1}$"]


count = 0
count_2 = 0
with open("/Users/thomasbekman/Documents/Research/Passwords/Cracked_Passwords/rockyou.txt", encoding="latin-1") as f:
    for line in f:

        #print(line.decode("latin-1"))
        for regex in regexList:
            print("Im the Rgex:   "+ regex)

            if(re.match(regex,str(line)) is not None):
                print(regex)
                print("---------------")
                print(line)
                count +=1
                break
            if(len(str(line)) == 2):
                count_2 +=1

print(str(count))
print(str(count_2))
'''