import re

'''
The purpose of this script is to analyze the coverage that regex's provide.
A little more specific is:
What percent of length 13 words are described by the top regular expressions imported from the Regex_toFormat.txt
'''


#To get exact regex match wrap the regex in ^ and $


#Function to read through regex file, and format it correctly (with prepending ^ and appending $, for exact matching
regexList = []
with open ("/Users/thomasbekman/Documents/Research/Regex_toFormat.txt") as f:
    for line in f:
        formattedLine = "^" + line[:-1] + "$" #The [:-1] is to deal with new lin charecters


        if (line.find("\n") == -1):
            formattedLine = "^"  + line + "$"
        regexList.append(formattedLine)



count_2 = 0
count_r_2 = 0

count_3 = 0
count_r_3 = 0

count_4 = 0
count_r_4 = 0

count_5 = 0
count_r_5 = 0

count_6 = 0
count_r_6 = 0


count_7 = 0
count_r_7 = 0


count_8 = 0
count_r_8 = 0


count_9 = 0
count_r_9 = 0

count_10 = 0
count_r_10 = 0

count_11 = 0
count_r_11 = 0

count_12 = 0
count_r_12 = 0

count_13 = 0
count_r_13 = 0

rockYouLength =  10000000
iter_count =0
with open("/Users/thomasbekman/Documents/Research/Passwords/Cracked_Passwords/mySpace.txt", encoding="latin-1") as f:
    for line in f:
        line = line.strip() #Removes new line charecters
        iter_count +=1
        if (iter_count  % 100000 == 0):
            print(str(iter_count/rockYouLength * 100) + str("% Done"))

        if(len(line) == 2):
            count_2 +=1

        if (len(line) == 3):
            count_3 += 1

        if (len(line) == 4):
            count_4 += 1

        if (len(line) == 5):
            count_5 += 1

        if (len(line) == 6):
            count_6 += 1

        if (len(line) == 7):
            count_7 += 1

        if (len(line) == 8):
            count_8 += 1

        if (len(line) == 9):
            count_9 += 1

        if (len(line) == 10):
            count_10 += 1

        if (len(line) == 11):
            count_11 += 1

        if (len(line) == 12):
            count_12 += 1

        if (len(line) == 13):
            count_13 += 1


        for regex in regexList:
           # print("Im the Rgex:   "+ regex)

            if(re.match(regex,str(line)) is not None):
                if (len(line) == 2):
                    count_r_2 += 1

                if (len(line) == 3):
                    count_r_3 += 1

                if (len(line) == 4):
                    count_r_4 += 1

                if (len(line) == 5):
                    count_r_5 += 1

                if (len(line) == 6):
                    count_r_6 += 1

                if (len(line) == 7):
                    count_r_7 += 1

                if (len(line) == 8):
                    count_r_8 += 1

                if (len(line) == 9):
                    count_r_9 += 1

                if (len(line) == 10):
                    count_r_10 += 1

                if (len(line) == 11):
                    count_r_11 += 1

                if (len(line) == 12):
                    count_r_12 += 1

                if (len(line) == 13):
                    count_r_13 += 1
                break
try:
    print("Length 2.......")
    print(str(count_r_2/count_2 * 100)  +"%")
    print("---------------------")
    print("                     ")
except:
    pass

try:
    print("Length 3.......")
    print(str(count_r_3/count_3 * 100)  +"%")
    print("---------------------")
    print("                     ")
except:
    pass

try:
    print("Length 4.......")
    print(str(count_r_4/count_4 * 100)  +"%")
    print("---------------------")
    print("                     ")

except:
    pass

try:
    print("Length 5.......")
    print(str(count_r_5/count_5 * 100)  +"%")
    print("---------------------")
    print("                     ")
except:
    pass

try:
    print("Length 6.......")
    print(str(count_r_6/count_6 * 100)  +"%")
    print("---------------------")
    print("                     ")
except:
    pass

try:
    print("Length 7.......")
    print(str(count_r_7/count_7 * 100)  +"%")
    print("---------------------")
    print("                     ")
except:
    pass

try:
    print("Length 8.......")
    print(str(count_r_8/count_8 * 100)  +"%")
    print("---------------------")
    print("                     ")
except:
    pass

try:
    print("Length 9.......")
    print(str(count_r_9/count_9 * 100)  +"%")
    print("---------------------")
    print("                     ")
except:
    pass

try:
    print("Length 10.......")
    print(str(count_r_10/count_10 * 100)  +"%")
    print("---------------------")
    print("                     ")
except:
    pass

try:
    print("Length 11.......")
    print(str(count_r_11/count_11 * 100)  +"%")
    print("---------------------")
    print("                     ")
except:
    pass

try:
    print("Length 12.......")
    print(str(count_r_12/count_12 * 100)  +"%")
    print("---------------------")
    print("                     ")
except:
    pass
try:
    print("Length 13.......")
    print(str(count_r_13/count_13 * 100)  +"%")
    print("---------------------")
    print("                     ")
except:
    pass