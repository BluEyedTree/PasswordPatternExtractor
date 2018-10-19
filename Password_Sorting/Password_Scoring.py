
import pymongo
from pymongo import MongoClient
import re
import Password_Sorting.extract_top_x_percent_substring as extract_top_x_percent_substring
import Password_Sorting.Utils as Utils
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
    return 1.6**(10*normalization)



'''
If the substring does not exist then a 0 is returned
If the DB value is greater than the cutoff then a 1 is returned
If the substring exists then its hitCount/cutOff is returned
'''
cutOff =  extract_top_x_percent_substring.determinePercentageCutoff(0.1)
def normalizeSubstringFrequency(password):
    db = client[SUBSTRING_DATABASE]
    collection = db[SUBSTRING_COLECTION]
    if(collection.find_one({"_id":password}) is None):
        return 0

    if(collection.find_one({"_id":password})['value']>cutOff):
        return 1
    else:
        return collection.find_one({"_id":password})['value']/cutOff


'''
Takes the input password and sees if it corresponds to one of the Regex's
If it corresponds to one of the regex's then a score is returned.
If its in the top 20% percent (as defined in the cutoff) then a 1 is returned
If its in the bottom 80% then regex  hitCount/cutOff is returned
'''
cutOff_regex =  extract_top_x_percent_substring.determinePercentageCutoff_For_Regex(0.2)
def normalizeRegexFrequency(regex):
    db = client[REGEX_DATABASE]
    collection = db[REGEX_COLLECTION]
    if(collection.find_one({"_id":regex}) is None):
        return 0

    if(collection.find_one({"_id":regex})['value']>cutOff_regex):
        return 1
    else:
        return collection.find_one({"_id":regex})['value'] / cutOff_regex

'''
Parameter 2 Substring coverage

Fi = Normalized frequency (number of times that substring was seen in the data, substring “hits”) of a substring
If the frequency is in the top 10%:
Fi = 1
If frequency in bottom 90%:
Fi =      Substring_Fi / Frequency that occurs directly at 80%

_L = Length of password uncovered. The number of chars in the password that are not seen in the substring DB.
Li = Length of the substring

S =  sum(Li * Fi)/ (sum(Li) +_L)

Score = 1.5^10(1-S)

Justification: This gives preference to passwords with uncommon substrings, for example iloveyou# is a bad password because iloveyou is very common substring. xyzwtxax is a better password than iloveyou, because of dictionary attacks.
Input Password
Output score
'''

def common_substring_coverage(password):
    db = client[SUBSTRING_DATABASE]
    collection = db[SUBSTRING_COLECTION]
    password_length = len(password)
    substringList = []

    substrings = Utils.subStringFinder(password)
    # Check if substring is in the DB, and has a frequency greater than 1

    for obj in substrings:
        if (collection.find_one({"_id": obj}) is not None
                and collection.find_one({"_id": obj})["value"] > 1):
            substringList.append(obj)

    # Find out how much of the password is covered by substrings
    for substring in substringList:
        chars = list(substring)
        for char in chars:
            password = password.replace(char, "")

    uncovered = len(password)

    numerator = 0.0  # sum(Li * Fi)
    denominator = 0.0  # sum(Li) +_L

    for substring in substringList:
        normalized_frequency = normalizeSubstringFrequency(substring)
        substring_length = len(substring)
        numerator += substring_length * normalized_frequency

        denominator += substring_length

    denominator = denominator + uncovered


    score = 1.5 ** ((1 - (numerator / denominator)) * 10)
    return score

'''
Parameter 3: Association rules coverage

Li = Length of the total association rule. This includes text before and after the arrow
Ci = The confidence value of the association rule
_L=   Length of password uncovered. The number of chars in the password that are not seen in the association rules DB

A = sum(Li*Ci) / (sum(Li) +_L)

Score: 
1.4^10(1-A)
'''
#The code is outside the method to prevent uneccesary repitition
db = client[ASSOCIATION_RULES_DATABASE]
collection = db[ASSOCIATION_RULES_COLLECTION]
associations_from_database = []
for obj in collection.find():
    association_rule = obj["_id"]
    confidence = obj["value"]
    first_word = association_rule.split("->")[0]
    second_word = association_rule.split("->")[1]
    associations_from_database.append((first_word,second_word,confidence))

def association_rule_coverage(password):

    association_rule_list = []
    for firstWord, secondWord, confidenceVal in associations_from_database:
        if firstWord in password and secondWord in password \
                and password.find(firstWord) < password.find(secondWord):
            association_rule_list.append((firstWord, secondWord, confidenceVal))

    # Both association rules need to be in the password. And if the association rule
    password_to_modify = password

    for first_word, second_word, con in association_rule_list:
        # We want to remove all the chars from both the 1st and 2nd word
        chars_to_remove = list(first_word) + list(second_word)
        for char in chars_to_remove:
            password_to_modify = password_to_modify.replace(char, "")
            password_to_modify = password_to_modify.replace(char, "")

    numerator = 0
    denominator = 0

    for Fword, Sword, conf in association_rule_list:
        association_rule_length = len(Fword) + len(Sword)
        numerator += association_rule_length * float(conf)
        denominator += association_rule_length

    uncovered_by_association_rules = len(password_to_modify)


    denominator += uncovered_by_association_rules




    return 1.4 ** ((1 - (numerator / denominator)) * 10)


'''
Parameter 4: Regex Coverage
Fi - Normalized Frequency(The number of times this regex was hit)
If Frequency of Regex in the top 20%:
Fi = 1
If Frequency In the bottom 80%:
Fi = Regex_Fi / Frequency that occurs directly at 80%

Score = 1.3^10(1-Fi)
'''

#Outside the method to allow regex's from db to be built once, instead of for every password
db = client[REGEX_DATABASE]
collection = db[REGEX_COLLECTION]
regex_list = []
for regex in collection.find():
    regex_list.append(regex)


def regex_rulecoverage(password):
    for regeX in regex_list:
        if(re.match(regeX["_id"], password) is not None):
            return 1.3**(10*(1-normalizeRegexFrequency(regeX["_id"])))


    return 1.3 ** (10 * (1 - 0)) #The case when the regex is not in the DB

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
            '''
            print(line)
            print(p1_score)
            print(p2_score)
            print(p3_score)
            print(p4_score)
            print("+-------+")
            '''
            totalScore = p1_score + p2_score + p3_score + p4_score
            tuple_to_add = (totalScore, p1_score, p2_score, p3_score, p4_score, line)
            totalList.append(tuple_to_add)
            if(iter_count %243423 == 0):
                f = open('scores.pkl', 'wb+')  # Pickle file is newly created where foo1.py is         # dump data to f
                pickle.dump(totalList, f)
                f.close()
    #sorts on the first value, which in this case is the total score
    totalList = sorted(totalList, key=lambda x: x[0], reverse=True)
    f = open('scores_WithUpdatedScores.pkl', 'wb')   # Pickle file is newly created where foo1.py is         # dump data to f
    pickle.dump(totalList,f)
    f.close()





#main("/Users/thomasbekman/Documents/Research/Passwords/Cracked_Passwords/UTF8_Formatted.txt")

#f = open('scores.pkl', 'rb')  # 'r' for reading; can be omitted
#value_list = pickle.load(f)  # load file content as mydict



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

#print(normalizeSubstringFrequency("c12"))
#print(common_substring_coverage("BlackJack12"))
