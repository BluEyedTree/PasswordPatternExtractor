import Markov_Attempt.treeForMarkov as tree

import Markov_Attempt.Markov as Markov
import Markov_Attempt.pwd_guess as pg
from unittest.mock import Mock, MagicMock
import numpy as np
import Markov_Attempt.treeForMarkov as tree
import sys



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
association_rules = read_association_rules_into_memory("/Users/thomasbekman/Documents/Research/SpadeFiles/MinSup20000,MinConf0.1_HalfData/Patterns_halfData.txt")



'''
This method modifies the probabilies returned by the markov model to include information about the known assocation rules
       
        You need to build a new dict, instead of changing the one you're iterating over.
        Step one build the word. Current + Char_from_prob_vector
        Step 2: Then check if the word satisfys assocation rules
        Step 3: Change its probability (figure out algorithm to do this
        
We include a scaleValue field which defines how much to multiply the confidence value by before using it to modify the probability returned by the markov model. 
The goal is to try different confidence values (0.1 -> 1) and use linear regression to find the best values (this same scale value will also be used with common substrings)

'''
def add_assocation_rules_to_prob(currentPassword, probability_vector, path__to_association_rules, scaleValue):
    assocation_probabilties = {}
    for char,probability in probability_vector.items():
        assocation_probabilties[char] = probability

        for rule in association_rules:
            new_word = currentPassword + char
            if(rule[0] in new_word and rule[1] in new_word):
                first_string_end_position = new_word.find(rule[0]) + len(rule[0])-1 #The first word in the association rules
                second_string_start_position = new_word.find(rule[1])

                if(second_string_start_position > first_string_end_position):
                    #TODO: Write a more intelligent scoring rule for the association rules
                    confidence_value = rule[3]
                    assocation_probabilties[char] = probability + (confidence_value*scaleValue)



        return assocation_probabilties







'''
A utility method that takes in the charbag, and probabilities as inputs. It returns the chars, along with their probabilties
'''
def probabilityToChar(charbag, probabilities):
    char_probs = {}
    for i in enumerate(probabilities):
        if i[1] != 0:
            #char_probs.append((charbag[i[0]],i[1]))
            char_probs[charbag[i[0]]] = i[1]
    return char_probs


config = Mock()
config.char_bag = pg.PASSWORD_END + 'abcdefghiklmnopqrst' + pg.PASSWORD_START + "ABCDEFGHIJKLMNOPQRSTRUV"
m = Markov.MarkovModel(config, smoothing='none', order=3)
m.train([('passA', 1), ('past', 1), ('ashen', 1), ('ass', 1), ('blah', 1), ('password', 10),('passwords', 10)])
answer = np.zeros((len(config.char_bag), ), dtype=np.float64)
m.predict('', answer)



root_node = tree.Node("",1)
sys.setrecursionlimit(50000)
def markovBuilder(currentNode, maxPasswordLength=10):
    config = Mock()
    #TODO: Add full character set to the char bag
    config.char_bag = pg.PASSWORD_END + 'abcdefghiklmnopqrst' + pg.PASSWORD_START + "ABCDEFGHIJKLMNOPQRSTRUV"
    answer = np.zeros((len(config.char_bag),), dtype=np.float64)
    if ("\n" not in currentNode.value and len(currentNode.value)<=maxPasswordLength):
        m.predict(currentNode.value, answer)
        char_to_add = probabilityToChar(m.alphabet, answer)
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
        passwords.append(node.value)
getPasswords(root_node)
print(passwords)