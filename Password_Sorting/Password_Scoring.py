
import pymongo
from pymongo import MongoClient
import re
import extract_top_x_percent_substring
import Utils
from datetime import datetime
import pickle


#MongoDB information
SUBSTRING_DATABASE = "Substring_Research"
SUBSTRING_COLECTION = "substring_Length3to8"

ASSOCIATION_RULES_DATABASE = "Association_Rules"
ASSOCIATION_RULES_COLLECTION = "Association_Rules_half_data_0.1_Confidence"

REGEX_DATABASE = "Research_Initial_Test"
REGEX_COLLECTION = "regex"

#MongoDB objects
client = MongoClient('localhost', 27017)


'''
Scoring based on length
Password length, L: normalize to 10 for example
L = 8 --> Normalized Length : 0.8
L >= 10 --> Normalized length : 1


parameter one P1: exponential score of goodness in length of password (2^10NL)
   NL = 0.0 --> P1 = 0
   NL = 1.0 --> P1 = 2^10 almost eq 1000


justification: password length has the most effect on goodness of a password.

Input: password string
Output: Score based on the password length
'''
def password_score_based_on_length(password):
    #Do normalization first
    normalization = len(password)/10

    if(len(password) >= 10):
        normalization = 1.0
    else:
        normalization = float(len(password))/float(10.0)
    return 2**(10*normalization)



'''
parameter two P2: not covered by any common substring

example: iloveyou123#, only # is not common, so uncovered length = 1
p2 = 1.5^(1/12 * 5)

In general, UL/L
P2 = 1.5^(UL/L * 10)

* UL: uncovered length

Justification: This gives preference to passwords with uncommon substrings, for example iloveyou# is a bad password because iloveyou is very common substring. xyzwtxax is a better password than iloveyou, because of dictionary attacks.
Input Password
Output score
'''

cutOff =  extract_top_x_percent_substring.determinePercentageCutoff(0.0001)
#TODO: Deal with the edge case in your evernotes.
def common_substring_coverage(password):
    db = client[SUBSTRING_DATABASE]
    collection = db[SUBSTRING_COLECTION]

    password_length = len(password)
    substringList = []

    substrings = Utils.subStringFinder(password)
    for obj in substrings:
        if(collection.find_one({"_id":obj}) is not None
                and collection.find_one({"_id":obj})["value"] >= cutOff):
            substringList.append(obj)

    for substring in substringList:
        chars = list(substring)
        for char in chars:
            password = password.replace(char, "")


    uncovered = len(password)
    score = 1.5**((uncovered/password_length) * 10)
    return score




'''
parameter three P3: length of uncovered by association rules (UAL)
In general, UL/L
P3 = 1.4^(UAL/L * 10)


lovehate
iloveyou

*This iterates through all mined association rules.

Justification: These two passwords have 0 uncommon substrings, however, love567 is a better password than iloveyou, because ilove and you cooccur in many passwords.
'''
#The code is outside the method to prevent uneccesary repitition
db = client[ASSOCIATION_RULES_DATABASE]
collection = db[ASSOCIATION_RULES_COLLECTION]
associations_from_database = []
for obj in collection.find():
    association_rule = obj["_id"]
    first_word = association_rule.split("->")[0]
    second_word = association_rule.split("->")[1]
    associations_from_database.append((first_word,second_word))

def association_rule_coverage(password):

    association_rule_list = []
    for firstWord, secondWord  in associations_from_database:
        if firstWord in password and secondWord in password \
                and password.find(firstWord) < password.find(secondWord):
            association_rule_list.append((firstWord,secondWord))

    #Both association rules need to be in the password. And if the association rule
    password_to_modify = password


    for first_word, second_word in association_rule_list:
        #We want to remove all the chars from both the 1st and 2nd word
        chars_to_remove = list(first_word) + list(second_word)
        for char in chars_to_remove:
            password_to_modify = password_to_modify.replace(char, "")
            password_to_modify = password_to_modify.replace(char, "")

    uncovered_by_association_rules = len(password_to_modify)
    return(1.4**(uncovered_by_association_rules/len(password) * 10))


'''
parameter four P4: normalized aggregate commonality of password pattern
love12 matches l4d2 and l*d*. This is regex!

assumption: all small letter is more frequent than small letters followed by numbers > numbers followed by small letters.

CS: commonness score of a pattern [0, 1]
0 --> not common at all
1 --> very common.

P4 = 1.3^(10*(1 - CS))

all digit passwords are very common.
justification: this puts emphasis on diversity of password structure, rather than just having symbols or digits in the password. If a password has a pattern that is very uncommon, it must have a highest score.

We argue that P1 more important than P2, more important than P3, more important than P4.
'''

#Outside the method to allow regex's from db to be built once, instead of for every password
db = client[REGEX_DATABASE]
collection = db[REGEX_COLLECTION]
regex_list = []
for regex in collection.find():
    regex_list.append(regex)

def regex_rulecoverage(password):
    db = client[REGEX_DATABASE]
    collection = db[REGEX_COLLECTION]

    commonFlag = 0
    for regeX in regex_list:
        if(re.match(regeX["_id"], password) is not None):
            commonFlag = 1

    return 1.3**(10*(1-commonFlag))



'''
THe main function runs all the rule coverage on an input list.
It saves the data as a list in the following format:
[(totalScore, p1_score, p2_score, p3_score, p4_score, word)]
'''
def main(filePath):
    totalList = []
    iter_count = 0
    rockYouLength = 24342374

    with open(filePath, encoding="utf-8") as infile:
        for line in infile:
            # print(line)
            iter_count += 1
            if (iter_count % 100 == 0):
                print(str(iter_count / rockYouLength * 100) + str("% Done"))
            line = line.rstrip("\n")

            p1_score = password_score_based_on_length(line)
            p2_score = common_substring_coverage(line)
            p3_score = association_rule_coverage(line)
            p4_score = regex_rulecoverage(line)
            totalScore = p1_score + p2_score + p3_score + p4_score
            tuple_to_add = (totalScore, p1_score, p2_score, p3_score, p4_score, line)
            totalList.append(tuple_to_add)
    #sorts on the first value, which in this case is the total score
    totalList = sorted(totalList, key=lambda x: x[0], reverse=True)
    f = open('scores.pkl', 'wb')   # Pickle file is newly created where foo1.py is         # dump data to f
    pickle.dump(totalList,f)
    f.close()

main("/Users/thomasbekman/Documents/Research/Passwords/Cracked_Passwords/UTF8_Formatted.txt")

f = open('scores.pkl', 'rb')  # 'r' for reading; can be omitted
value_list = pickle.load(f)  # load file content as mydict
#print(value_list)
'''

#print(extract_top_x_percent_substring.determinePercentageCutoff(0.2))
#print(common_substring_coverage("abc123"))
startTime = datetime.now()

#Coverage 2, length 4
print(password_score_based_on_length("abc123"))
print(common_substring_coverage("abc123"))

print(association_rule_coverage("abc123"))
print(regex_rulecoverage("abc123"))
#print((datetime.now() - startTime).total_seconds())

'''