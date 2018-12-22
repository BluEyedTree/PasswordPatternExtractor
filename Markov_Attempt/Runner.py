import Markov_Attempt.treeForMarkov as tree

import Markov_Attempt.Markov as Markov
import Markov_Attempt.pwd_guess as pg
from unittest.mock import Mock, MagicMock
import numpy as np
import Markov_Attempt.treeForMarkov as tree
import sys

'''
A utility method that takes in the charbag, and probabilities as inputs. It returns the chars, along with their probabilties
'''
def probabilityToChar(charbag, probabilities):
    char_probs = []
    for i in enumerate(probabilities):
        if i[1] != 0:
            char_probs.append((charbag[i[0]],i[1]))
    return char_probs


config = Mock()
config.char_bag = pg.PASSWORD_END + 'abcdefghiklmnopqrst' + pg.PASSWORD_START + "ABCDEFGHIJKLMNOPQRSTRUV"
m = Markov.MarkovModel(config, smoothing='none', order=3)
m.train([('passA', 1), ('past', 1), ('ashen', 1), ('ass', 1), ('blah', 1), ('password', 10)])

answer = np.zeros((len(config.char_bag), ), dtype=np.float64)
m.predict('', answer)



root_node = tree.Node("",1)
sys.setrecursionlimit(50000)
def markovBuilder(currentNode, maxPasswordLength=10):
    config = Mock()
    config.char_bag = pg.PASSWORD_END + 'abcdefghiklmnopqrst' + pg.PASSWORD_START + "ABCDEFGHIJKLMNOPQRSTRUV"
    answer = np.zeros((len(config.char_bag),), dtype=np.float64)
    if ("\n" not in currentNode.value and len(currentNode.value)<=maxPasswordLength):
        m.predict(currentNode.value, answer)
        char_to_add = probabilityToChar(m.alphabet, answer)
        for char, probability in char_to_add:
            newString = currentNode.value + char
            new_node_to_add = tree.Node(newString,probability)
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


'''

print("test")
for i in root_node.getChildren():
    print(i.value,i.priority)


print("test")

getPasswords(root_node)
print("!!!")
print(passwords)
print("!!!!!")
for i in passwords:
    print(i)
    
'''
'''
print(root_node.getChildren())
for i in root_node.getChildren():
    print(i.value)

'''
'''
current_node = root_node
while current_node.getChildren() != []:
    print(current_node.getChildren())
'''
'''

passwordList = []
def getPasswords(currentNode):
    if(currentNode.getChildren != []):
        for sibling in currentNode.getChildren():
            getPasswords(sibling)
'''

