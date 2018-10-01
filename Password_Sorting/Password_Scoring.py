
import pymongo
from pymongo import MongoClient


#MongoDB information
SUBSTRING_DATABASE = "test"
SUBSTRING_COLECTION = "test"

ASSOCIATION_RULES_DATABASE = "Association_Rules"
ASSOCIATION_RULES_COLLECTION = "Association_Rules_half_data_0.1_Confidence"

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
    normalization = 0
    if(len(password) >= 10):
        normalization = 1.0
    else:
        normalization = len(password)/10
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


def common_substring_coverage(password):
    db = client[SUBSTRING_DATABASE]
    collection = db[SUBSTRING_COLECTION]

    password_length = len(password)
    substringList = []
    for obj in collection.find().sort([('value', pymongo.DESCENDING)]):
        if(obj["_id"] in password):
            substringList.append(obj["_id"])

    sorted_substringList = sorted(substringList, key=len, reverse=True)

    for substring in sorted_substringList:
        if (substring in password):
            password = password.replace(substring, "")


    uncovered = len(password)
    #Score might be incorrect, I'm not sure if coveragfirstANNModele/not coverage
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
def association_rule_coverage(password):
    db = client[ASSOCIATION_RULES_DATABASE]
    collection = db[ASSOCIATION_RULES_COLLECTION]

    association_rule_list = []
    for obj in collection.find():
        association_rule = obj["_id"]
        first_word = association_rule.split("->")[0]
        second_word = association_rule.split("->")[1]
        if first_word in password and second_word in password:
            association_rule_list.append((first_word,second_word))

    #Both association rules need to be in the password. And if the association rule
    password_to_modify = password
    for first_word, second_word in association_rule_list:
        if (first_word in password_to_modify  and second_word in password_to_modify and password_to_modify.find(first_word) < password_to_modify.find(second_word)):
            password_to_modify = password_to_modify.replace(first_word, "")
            password_to_modify = password_to_modify.replace(second_word, "")


    uncovered_by_association_rules = len(password_to_modify)
    print(1.4**(uncovered_by_association_rules/len(password) * 10))






#Coverage 2, length 4
print(password_score_based_on_length("castr"))
print(common_substring_coverage("castr"))

association_rule_coverage("dancseexy")