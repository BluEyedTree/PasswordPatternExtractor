
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
    import pymongo
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)
    db = client["test"]
    collection = db["test"]

    password_length = len(password)
    substringList = []
    for obj in collection.find().sort([('value', pymongo.DESCENDING)]):
        if(obj["_id"] in password):
            substringList.append(obj["_id"])

    sorted_substringList = sorted(substringList, key=len, reverse=True)

    for substring in sorted_substringList:
        if (substring in password):
            password = password.replace(substring, "")


    coverage = password_length-len(password)
    #Score might be incorrect, I'm not sure if coverage/not coverage
    score = 1.5**((coverage/password_length) * 10)
    return score

#Coverage 2, length 4
print(common_substring_coverage("cast"))