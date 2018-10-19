import Password_Sorting.Password_Scoring
import Password_Sorting.extract_top_x_percent_substring
import Password_Sorting.Utils as Utils
import re

from pymongo import MongoClient
import math

def test_normalizeSubstringFrequency():
    SUBSTRING_DATABASE = "test"
    SUBSTRING_COLECTION = "Substring_test"
    client = MongoClient('localhost', 27017)
    cutOff = 2

    def normalizeSubstringFrequency(password):
        db = client[SUBSTRING_DATABASE]
        collection = db[SUBSTRING_COLECTION]
        if (collection.find_one({"_id": password}) is None):
            return 0

        if (collection.find_one({"_id": password})['value'] > cutOff):
            return 1
        else:
            return collection.find_one({"_id": password})['value'] / cutOff


    assert normalizeSubstringFrequency("ab") == 1 and normalizeSubstringFrequency("c12") == 0.5 and  normalizeSubstringFrequency("@") == 0



def test_common_substring_coverage1():
    SUBSTRING_DATABASE = "test"
    SUBSTRING_COLECTION = "Substring_test"
    client = MongoClient('localhost', 27017)


    def common_substring_coverage1(password):
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
            normalized_frequency = Password_Sorting.Password_Scoring.normalizeSubstringFrequency(substring)
            substring_length = len(substring)
            numerator += substring_length * normalized_frequency

            denominator += substring_length

        denominator = denominator + uncovered


        score = 1.5 ** ((1 - (numerator / denominator)) * 10)
        return score

    assert common_substring_coverage1("Madeb123") == 1
    assert round(common_substring_coverage1("abc1234")) == 10

#TODO:Write tests that use that actual association rule DB
def test_common_association_coverage1():
    client = MongoClient('localhost', 27017)
    db = client["test"]
    collection = db["association_rules_test"]
    associations_from_database = []
    for obj in collection.find():
        association_rule = obj["_id"]
        confidence = obj["value"]
        first_word = association_rule.split("->")[0]
        second_word = association_rule.split("->")[1]
        associations_from_database.append((first_word, second_word, confidence))

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


        print(password)
        print("SCORE")
        print(1.4 ** ((1 - (numerator / denominator)) * 10))


        return 1.4 ** ((1 - (numerator / denominator)) * 10)

    assert math.floor(association_rule_coverage("appman")) == 15
    assert math.floor(association_rule_coverage("ap!pman")) == 16




def test_determinePercentageCutoff_For_Regex():
    cutOff_regex = Password_Sorting.extract_top_x_percent_substring.determinePercentageCutoff_For_Regex(0.2)
    client = MongoClient('localhost', 27017)
    REGEX_DATABASE = "Research_Initial_Test"
    REGEX_COLLECTION = "regex"
    def normalizeRegexFrequency(regex):
        db = client[REGEX_DATABASE]
        collection = db[REGEX_COLLECTION]
        print("!!!!!!!")
        print(cutOff_regex)
        print()
        if (collection.find_one({"_id": regex}) is None):
            return 0

        if (collection.find_one({"_id": regex})['value'] > cutOff_regex):
            return 1
        else:
            return collection.find_one({"_id": regex})['value'] / cutOff_regex

    assert normalizeRegexFrequency("^[a-z]{6}$") == 1
    assert normalizeRegexFrequency("^[A-Za-z0-9]{2}$") < 0.001


def test_regex_rulecoverage():
    REGEX_DATABASE = "Research_Initial_Test"
    REGEX_COLLECTION = "regex"
    client = MongoClient('localhost', 27017)
    db = client[REGEX_DATABASE]
    collection = db[REGEX_COLLECTION]
    regex_list = []
    for regex in collection.find():
        regex_list.append(regex)

    def regex_rulecoverage(password):
        for regeX in regex_list:
            if (re.match(regeX["_id"], password) is not None):
                return 1.3 ** (10 * (1 - Password_Sorting.Password_Scoring.normalizeRegexFrequency(regeX["_id"])))

        return 1.3 ** (10 * (1 - 0))  # The case when the regex is not in the DB
    assert regex_rulecoverage("abcdef") == 1
    assert regex_rulecoverage("dasdasdasdasdasdasdas245#$") > 13


#TODO: Add one more test to test_regex-_rulecoverage(). Test a non 1 case.

