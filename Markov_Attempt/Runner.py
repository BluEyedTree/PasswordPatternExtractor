import Markov_Attempt.treeForMarkov as tree

import Markov_Attempt.Markov as Markov
import Markov_Attempt.pwd_guess as pg
from unittest.mock import Mock, MagicMock
import numpy as np
import Markov_Attempt.treeForMarkov as tree
import sys
from pymongo import MongoClient
import time
import Password_Sorting.Password_Scoring as Scoring
import string

#TODO: Should paswords used for training have the start and end characters?
def generate_dataset_from_textfile(textfile_path):
    words_dict = {}
    list_to_return = []
    text_file = open(textfile_path,"r")
    for word in text_file:
        if word in words_dict:
            words_dict[word.strip()] += 1
        else:
            words_dict[word.strip()] = 1

    for key,value in words_dict.items():
        list_to_return.append(("\t"+key,value))


    return list_to_return



print(generate_dataset_from_textfile("/Users/thomasbekman/Desktop/pass.txt"))

def read_association_rules_into_memory(path__to_association_rules):
    association_rules = []
    with open(path__to_association_rules) as f:
        lines = f.readlines()
    for line in lines:
        score = float(line.split(",")[1])
        first_word = line.split("->")[0]
        second_word = line.split("->")[1].split(",")[0]
        association_rules.append((first_word,second_word,score))

    return association_rules


def read_common_substrings_into_memory(cutoff):
    client = MongoClient('localhost', 27017)
    db = client['Substring_Research']  # Might have to change this back to mydb
    collection = db["substring_Length3to8"]
    #Based on running extract_top_x_Percentage substring it was found that the top %1 of common substrings happen over 176
    start_time = time.time()
    substrings_cursor =  collection.find({"value":{"$gt": cutoff}})#Returns all items where the value is greater than 76
    list_to_return = list(substrings_cursor)
    print("Mongo", time.time() - start_time, "s to run")

    return list_to_return

#Call not needed if using the new scoring function
#common_substrings = read_common_substrings_into_memory(200)
association_rules = read_association_rules_into_memory("/Users/thomasbekman/Documents/Research/SpadeFiles/MinSup20000,MinConf0.1_HalfData/Patterns_halfData.txt")



'''
This method modifies the probabilies returned by the markov model to include information about the known assocation rules
       
        You need to build a new dict, instead of changing the one you're iterating over.
        Step one build the word. Current + Char_from_prob_vector
        Step 2: Then check if the word satisfys assocation rules
        Step 3: Change its probability (figure out algorithm to do this
        
We include a scaleValue field which defines how much to multiply the confidence value by before using it to modify the probability returned by the markov model. 
The goal is to try different confidence values (0.1 -> 1) and use linear regression to find the best values (this same scale value will also be used with common substrings)

This also adds up all the scores seen for the current word. It doesn't take into account if the score is generated from a newly created assocation rule.
Is this the best approach?

!!!!! WARNING if this is slow its because of block that gets called before association rule coverage, removing that will speed up every call to Password_Scoring !!!!!!!!

Ideas on scale values to try
In a testing case a scale_value of 2 would double the probability
'''
def add_assocation_rules_to_prob(currentPassword, probability_vector, scaleValue):
    assocation_probabilties = {}
    for char,probability in probability_vector.items():
        assocation_probabilties[char] = probability

        for rule in association_rules:
            new_word = currentPassword + char
            #If you want to make this more stringent, then you should add the following to the if block:  and rule[1]  not in currentPassword
            #This would only increase the probability when the association rule is created with the addition of the letter. Instead of now where the probabilties are increased for every letter added after the creation of an association rule.
            if(rule[0] in new_word and rule[1] in new_word):
                first_string_end_position = new_word.find(rule[0]) + len(rule[0])-1 #The first word in the association rules
                second_string_start_position = new_word.find(rule[1])

                if(second_string_start_position > first_string_end_position):
                    assocation_probabilties[char] = assocation_probabilties[char] + (Scoring.association_rule_coverage(new_word)*scaleValue)



    return assocation_probabilties

start_time = time.time()

'''
TO TEST, ensures that probability goes up when adding an association rule.
fake_prob_vector = {"e":0.2, "a": 0.3, "p": 0.1, "12":0.1}
add_assocation_rules_to_prob("Pass0034",fake_prob_vector, 2)
'''
#add_common_substring_to_prob("Pass000",{"a":0.67, "b":0.333, "c":0.27, "de":0.1111},0.27 ,100000000000)
print ("Association check took", time.time() - start_time, "s to run")



'''
Cutoff scores will result in the same value being returned for all characters. Found that a cutoff=100000, added the ability to really see the difference. 
Also tests a scaling value of 0.27, which with the score was able to raise some values 28%
'''
#Cutoff at first should be 176 or top 1% of substrings
#TODO: Add code to automaticly determine cutoff, code exists in the password Sorting folder to do this.
def add_common_substring_to_prob(currentPassword, probability_vector, scaleValue, cutoff):

    assocation_probabilties = {}
    for char,probability in probability_vector.items():
        assocation_probabilties[char] = probability
        start_time = time.time()

        new_word = currentPassword + char
        assocation_probabilties[char] = assocation_probabilties[char] + (Scoring.common_substring_coverage(new_word, cutoff)) * scaleValue
    print("Iterating over the words took:", time.time() - start_time, "s to run")

    return assocation_probabilties

    #substring_list is a list of dictionaries. Where _id is string, and value is the hit count

print("sdaasdas")
#fake_prob_vector = {"e":0.2, "a": 0.3, "p": 0.1, "12":0.1}
#add_common_substring_to_prob("Pass0034",fake_prob_vector, 0.25, 0.2)



'''
Example usage that showed this works as expected. tie > tic > tif in terms of # of times these substrings appeared in the DB
You can see that the probabilities from the query below matches this. 

add_common_substring_to_prob("ti",{"a":0.1, "b":0.1, "c":0.1, "d":0.1, "e":0.1, "f":0.1, "g":0.1, "h":0.1, "i":0.1, "j":0.1, "k":0.1, "l":0.1, "s": 0.1, "ss": 0.1},0.27 ,100000)
'''

'''
A utility method that takes in the charbag, and probabilities as inputs. It returns the chars, along with their probabilties
'''

def add_common_regex_to_prob(currentPassword, probability_vector, scaleValue):

    assocation_probabilties = {}
    for char,probability in probability_vector.items():
        assocation_probabilties[char] = probability
        start_time = time.time()

        new_word = currentPassword + char
        new_word = new_word.strip()
        assocation_probabilties[char] = assocation_probabilties[char] + (Scoring.regex_rulecoverage(new_word)) * scaleValue
    print("Iterating over the words took:", time.time() - start_time, "s to run")

    return assocation_probabilties


#To Test common_regex

print("test Regex_to_prob")
start_time = time.time()
#add_common_regex_to_prob("Pass0034",fake_prob_vector, 0.25, 0.2)
print ("REGEX check took", time.time() - start_time, "s to run")


def probabilityToChar(charbag, probabilities):
    char_probs = {}
    for i in enumerate(probabilities):
        if i[1] != 0:
            #char_probs.append((charbag[i[0]],i[1]))
            char_probs[charbag[i[0]]] = i[1]
    return char_probs


config = Mock()

white_space_chars = set(string.whitespace)
all_chars = b = set(string.printable)
chars_to_use = list(all_chars - white_space_chars)
chars_to_use = "".join(chars_to_use)


config.char_bag = pg.PASSWORD_END +pg.PASSWORD_START + chars_to_use
m = Markov.MarkovModel(config, smoothing='none', order=3)
m.train([('\tpass+A', 5), ('\tpast', 1), ('\tashen', 1), ('\tas&^R$s', 1), ('\tbl+ah', 1),('\tbl+ahs', 1),('\tblhma', 1), ('\tblmag', 1)])
answer = np.zeros((len(config.char_bag), ), dtype=np.float64)
m.predict('', answer)



root_node = tree.Node("",1)
sys.setrecursionlimit(50000)
def markovBuilder(currentNode, maxPasswordLength=10):
    config = Mock()
    #TODO: Add full character set to the char bag
    config.char_bag = pg.PASSWORD_END +  pg.PASSWORD_START + chars_to_use
    answer = np.zeros((len(config.char_bag),), dtype=np.float64)
    if ("\n" not in currentNode.value and len(currentNode.value)<=maxPasswordLength):
        m.predict(currentNode.value, answer)
        char_to_add = probabilityToChar(m.alphabet, answer)
        #The lines below add our rules to the probabilties
        char_to_add =  add_common_substring_to_prob(currentNode.value, char_to_add, 0.25, 100000) #Adds substring probabilities
        char_to_add = add_assocation_rules_to_prob(currentNode.value,char_to_add, 2)
        char_to_add = add_common_regex_to_prob(currentNode.value, char_to_add, 0.25)

        for char, probability in char_to_add.items():

            newString = currentNode.value + char
            newProbability = probability * currentNode.priority #Multiplies the current probability with the parents. This way all the probabilties used to generate each string are taken into account

            new_node_to_add = tree.Node(newString,newProbability)
            currentNode.add_child(new_node_to_add)

        for child in currentNode.getChildren():
            markovBuilder(child)



markovBuilder(root_node)

'''
Goes through the tree the markov builder made, and returns the passwords in order into a list
'''
passwords = []
def getPasswords(node):
    if(node.getChildren() != []):
        for sibling in node.getChildren():
            getPasswords(sibling)
    else:
        passwords.append((node.priority,node.value))


def write_passwords_to_file(file_path):
    passwords.sort(reverse=True)
    with open(file_path, "w") as f:
        for password in passwords:
            f.write(str((password[0], password[1].strip()))+"\n")






getPasswords(root_node)
passwords.sort(reverse=True)
print(len(passwords))
write_passwords_to_file("/Users/thomasbekman/git/PasswordPatternExtractor/example.txt")


