import Markov_Attempt.Markov as Markov
import Markov_Attempt.pwd_guess as pg
from unittest.mock import Mock, MagicMock
import numpy as np

import time
import Password_Sorting.Password_Scoring as Scoring
import string
import math
import Password_Sorting.Utils as Utils
import Markov_Attempt.Association_Predicting_Markov as Association_markov
import Markov_Attempt.Utils as mem_utils


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
        list_to_return.append(("\t"+key+"\n",value))


    return list_to_return



#print(generate_dataset_from_textfile("/Users/thomasbekman/Desktop/pass.txt"))

#training_data = generate_dataset_from_textfile("/Users/thomasbekman/Documents/Research/Passwords/Cracked_Passwords/mySpace.txt")

training_data = generate_dataset_from_textfile("/Users/thomasbekman/Documents/Research/Passwords/Cracked_Passwords/1.txt")


#Call not needed if using the new scoring function
#common_substrings = read_common_substrings_into_memory(200)
association_rules = mem_utils.read_association_rules_into_memory("/Users/thomasbekman/Documents/Research/SpadeFiles/MinSup20000,MinConf0.1_HalfData/Patterns_halfData.txt")


def find_first_part_association_rules_for_string(password):
    assocation_rules_satisfied = []

    substrings = Utils.subStringFinder(password)


    for substring in substrings:
        if (substring in association_rules):
            for second_part_of_association in association_rules[substring].keys():
                assocation_rules_satisfied.append((substring, second_part_of_association))

    return assocation_rules_satisfied
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
def add_assocation_rules_to_prob(currentPassword,  char_to_add):
        association_prob = 0
        start_time = time.time()

        assocation_rules_satisfied = []

        new_word = currentPassword + char_to_add

        assocation_rules_satisfied = find_first_part_association_rules_for_string(new_word)


        for rule in assocation_rules_satisfied:

            #If you want to make this more stringent, then you should add the following to the if block:  and rule[1]  not in currentPassword
            #This would only increase the probability when the association rule is created with the addition of the letter. Instead of now where the probabilties are increased for every letter added after the creation of an association rule.
            if(rule[0] in new_word and rule[1] in new_word):
                first_string_end_position = new_word.find(rule[0]) + len(rule[0])-1 #The first word in the association rules
                second_string_start_position = new_word.find(rule[1])

                if(second_string_start_position > first_string_end_position):
                    association_prob = Scoring.association_rule_coverage(new_word)

        print("Association check took", time.time() - start_time, "s to run")
        return association_prob



'''
TO TEST, ensures that probability goes up when adding an association rule.
fake_prob_vector = {"e":0.2, "a": 0.3, "p": 0.1, "12":0.1}
add_assocation_rules_to_prob("Pass0034",fake_prob_vector, 2)
'''
#add_common_substring_to_prob("Pass000",{"a":0.67, "b":0.333, "c":0.27, "de":0.1111},0.27 ,100000000000)




'''
Cutoff scores will result in the same value being returned for all characters. Found that a cutoff=100000, added the ability to really see the difference. 
Also tests a scaling value of 0.27, which with the score was able to raise some values 28%
'''
#Cutoff at first should be 176 or top 1% of substrings
#TODO: Add code to automaticly determine cutoff, code exists in the password Sorting folder to do this.
def add_common_substring_to_prob(currentPassword, char_to_add,  cutoff):
        substring_prob = 0

        start_time = time.time()

        new_word = currentPassword + char_to_add
        substring_prob = Scoring.common_substring_coverage(new_word, cutoff)
        print("Substring Time:", time.time() - start_time, "s to run")

        return substring_prob

    #substring_list is a list of dictionaries. Where _id is string, and value is the hit count




'''
Example usage that showed this works as expected. tie > tic > tif in terms of # of times these substrings appeared in the DB
You can see that the probabilities from the query below matches this. 

add_common_substring_to_prob("ti",{"a":0.1, "b":0.1, "c":0.1, "d":0.1, "e":0.1, "f":0.1, "g":0.1, "h":0.1, "i":0.1, "j":0.1, "k":0.1, "l":0.1, "s": 0.1, "ss": 0.1},0.27 ,100000)
'''

'''
A utility method that takes in the charbag, and probabilities as inputs. It returns the chars, along with their probabilties
'''

def add_common_regex_to_prob(currentPassword, char_to_add):
    regex_prob = 0


    start_time = time.time()

    new_word = currentPassword + char_to_add
    new_word = new_word.strip()
    regex_prob = Scoring.regex_rulecoverage(new_word)
    print("Regex Time:", time.time() - start_time, "s to run")

    return regex_prob


#To Test common_regex

print("test Regex_to_prob")
start_time = time.time()
#add_common_regex_to_prob("Pass0034",fake_prob_vector, 0.25, 0.2)
print ("REGEX check took", time.time() - start_time, "s to run")



def calculate_weighted_average(markov_prob, association_prob,  regex_prob, markov_weight, association_weight, regex_weight):

    total_weight = association_weight  + regex_weight + markov_weight
    markov_contribution = markov_prob * markov_weight
    association_contribution = association_prob * association_weight
    #substring_contribution = substring_prob * substring_weight
    regex_contribution = regex_prob * regex_weight
    weighted_average = (association_contribution + regex_contribution + markov_contribution) / total_weight
    return  weighted_average

'''
Converts the probability vector into a char prediction dictionary.

This was modified to also check if an association word should be added. 
'''
def probabilityToChar(charbag, probabilities, current_word):
    char_probs = {}

    #Below are the lines I started using to implement random insertion of association rules.
    #For now leave it, and add better stats based approach later.
    '''

    assocation_rules_satisfied = find_first_part_association_rules_for_string(current_word)
    total_association_confidence = 0
    add_substring_to_add_association_rule = False
    association_string_to_add = []
    
    if(assocation_rules_satisfied != []):
        for rule in assocation_rules_satisfied:
            if (rule[0] in current_word and rule[1] not in current_word): #Want to guess it if the second part is not all ready in the word.
                total_association_confidence += association_rules[rule[0]][rule[1]]

    '''
    for i in enumerate(probabilities):
        if i[1] != 0 and i[1] != math.inf and not np.isnan(i[1]):
            char_probs[charbag[i[0]]] = i[1]
    return char_probs


#Below are a bunch of configurations for the markov model.
#TODO: Pull all this out and have it be configurable.
config = Mock()
white_space_chars = set(string.whitespace)
all_chars = b = set(string.printable)
chars_to_use = list(all_chars - white_space_chars)
chars_to_use = "".join(chars_to_use)


config.char_bag = list(pg.PASSWORD_END +pg.PASSWORD_START + chars_to_use)
config.char_bag.append("tar")
m = Markov.MarkovModel(config, smoothing='none', order=4)
#m.train([('\tpass+A', 5), ('\tpast', 1), ('\tashen', 1), ('\tas&^R$s', 1), ('\tbl+ah', 1),('\tbl+ahs', 1),('\tblhma', 1), ('\tblmag', 1)])
m.train(training_data)


print(m.freq_dict)
#answer = np.zeros((len(config.char_bag), ), dtype=np.float64)
#m.predict('', answer)

#probabilityToChar(config.char_bag, {}, "c123")

def pop_max(input_list):
    list1 = [input_list.pop(input_list.index(max(input_list)))]
    return list1

'''
Initalize first layer creates the first layer you want for you markov tree. 
It currently starts creating string from the empty string
'''

#The two vars below are used in the getNext function
current_layer = []
to_pop = []
def initialize_first_current_layer():
    global  current_layer

    answer = np.zeros((len(config.char_bag),), dtype=np.float64)
    m.predict("", answer)
    prediction_dict = probabilityToChar(m.alphabet, answer, "")


    for key in prediction_dict.keys():
        current_layer.append((prediction_dict[key],key))
'''
Calling this function returns you the next prediction. 
'''

def get_next(max_pwd_length):
    global current_layer
    global to_pop
    new_current = []
    if to_pop != []:
        return pop_max(to_pop)
    else:
        new_current = []
        for substring in current_layer:
            answer = np.zeros((len(config.char_bag)), dtype=np.float64)
            to_pop.append(substring)
            m.predict(substring[1], answer)
            prediction_dict =  probabilityToChar(m.alphabet, answer, substring)
            for prediction in prediction_dict.items():
                to_add_word = substring[1] + prediction[0]
                markov_prob = prediction[1]
                #substring_prob = add_common_substring_to_prob(substring[1], prediction[0],  100000)  # Adds substring probabilities
                association_prob = add_assocation_rules_to_prob(substring[1], prediction[0])
                regex_prob = add_common_regex_to_prob(substring[1], prediction[0])
                #Two lines below need to be run when weighted prob is working
                weighted_average_probs = calculate_weighted_average(markov_prob, association_prob ,regex_prob , 0.25, 0.25, 0.25) #TODO: Update this so it is no longer hard coded
                to_add_prob = substring[0] * weighted_average_probs #Mulitplies the current probability with that of the parent
                if len(to_add_word) <= max_pwd_length:
                    new_current.append((to_add_prob,to_add_word))
    current_layer = new_current
    return pop_max(to_pop)


#TODO: This probably needs to write to the mongoDB, or batch write a text file. All passwords should probably be made before the testing stage.
initialize_first_current_layer()
def generatePasswords():
    passwords = []
    try:
        while True:
            next_password = get_next(7) #Next password might not be the complete guess
            if "\n" in next_password[0][1]:
                prob = next_password[0][0]
                formatted_password = next_password[0][1].strip()
                passwords.append((prob,formatted_password))
    except:
        return passwords

'''
print("----")
print(generatePasswords())
print("----")
'''



print("Starting test below")




#a = Association_Prediction_Markov.Association_Prediction_Markov(5)
#a = Association_Prediction_Markov.Association_Prediction_Markov(5,training_data,"/Users/thomasbekman/Documents/Research/Passwords/Cracked_Passwords/1.txt")

#ab= Association_Predicting_Markov_2.test()
#a = Association_Predicting_Markov_2.Association_Prediction_Markov()
#a.update_charbag("1234567")
#print(a.charbag)

#a = Markov_Attempt.Association_Predicting_Markov.PASSWORD_START



'''

print("Starting large scale test")
start_time = time.time()







print("!!!!")
a = Association_markov.Association_Prediction_Markov(8,training_data,"/Users/thomasbekman/Documents/Research/SpadeFiles/MinSup20000,MinConf0.1_HalfData/Patterns_halfData.txt")
answer = a.predict("s34a")
#charbag, probabilities, current_word
print("Guess s34a" + str(probabilityToChar(a.charbag,answer,"Irrelavant arg")))

answer = a.predict("567")
#charbag, probabilities, current_word
print("Guess 567" + str(probabilityToChar(a.charbag,answer,"Irrelavant arg")))

answer = a.predict("567a")
#charbag, probabilities, current_word
print("Guess 567" + str(probabilityToChar(a.charbag,answer,"Irrelavant arg")))


answer = a.predict("567b")
#charbag, probabilities, current_word
print("Guess 567" + str(probabilityToChar(a.charbag,answer,"Irrelavant arg")))

answer = a.predict("567c")
#charbag, probabilities, current_word
print("Guess 567" + str(probabilityToChar(a.charbag,answer,"Irrelavant arg")))

answer = a.predict("567d")
#charbag, probabilities, current_word
print("Guess 567" + str(probabilityToChar(a.charbag,answer,"Irrelavant arg")))

for i in list(string.printable):
    answer = a.predict("567"+str(i))
    # charbag, probabilities, current_word
    print("Guess 567 " + str(i) + " " + str(probabilityToChar(a.charbag, answer, "Irrelavant arg")))

for i in list(string.printable):
    answer = a.predict("34"+str(i))
    # charbag, probabilities, current_word
    print("Guess 34 " + str(i) + " " + str(probabilityToChar(a.charbag, answer, "Irrelavant arg")))


for i in list(string.printable):
    answer = a.predict("hl"+str(i))
    # charbag, probabilities, current_word
    print("Guess hl " + str(i) + " " + str(probabilityToChar(a.charbag, answer, "Irrelavant arg")))


for i in list(string.printable):
    answer = a.predict("uv"+str(i))
    # charbag, probabilities, current_word
    print("Guess uv " + str(i) + " " + str(probabilityToChar(a.charbag, answer, "Irrelavant arg")))


for i in list(string.printable):
    answer = a.predict("uv"+str(i) +str(i))
    # charbag, probabilities, current_word
    print("Guess uv " + str(i) + str(i) +" " + str(probabilityToChar(a.charbag, answer, "Irrelavant arg")))

print ("Large Scale test took: ", time.time() - start_time, "s to run")



answer = a.predict("34a")
#charbag, probabilities, current_word
print("Guess 34a" + str(probabilityToChar(a.charbag,answer,"Irrelavant arg")))

answer = a.predict("34")
#charbag, probabilities, current_word
print("Guess 34" + str(probabilityToChar(a.charbag,answer,"Irrelavant arg")))



print("!!!!")
'''
a = Association_markov.Association_Prediction_Markov(8,training_data,"/Users/thomasbekman/Documents/Research/SpadeFiles/MinSup20000,MinConf0.1_HalfData/Patterns_halfData.txt")
answer = a.predict("3456")
#charbag, probabilities, current_word
print("Guess 34" + str(answer))
