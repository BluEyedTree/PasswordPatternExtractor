import Markov_Attempt.Markov as Markov
import Markov_Attempt.pwd_guess as pg
from multiprocessing import Pool
import multiprocessing
import glob
import json
from unittest.mock import Mock, MagicMock
import numpy as np
import sys
import time
import Password_Sorting.Password_Scoring as Scoring
import string
import math
import Password_Sorting.Utils as Utils
import Markov_Attempt.Association_Predicting_Markov as Association_markov
import Markov_Attempt.Utils as mem_utils
import collections
import Markov_Attempt.treeForMarkov as tree
from collections import deque

class config_mock():
    def __init__(self):
        self.charbag = []



class Create_Password_Guesses(collections.Iterator):

    def __init__(self, training_data_path=None, association_rule_path=None, char_markov_order=None, char_assocation_order=None, max_pwd_len=None, initilize_here = False):
        self.char_markov_order = char_markov_order

        if  training_data_path != None:
            self.training_data = self.generate_dataset_from_textfile(training_data_path)

        if association_rule_path != None:
            self.association_rule_path = association_rule_path
            self.association_rules = mem_utils.read_association_rules_into_memory(association_rule_path) #This requires a textfile


        self.max_pwd_len = max_pwd_len
        self.config = config_mock()
        #self.config.__class__ = Mock
        white_space_chars = set(string.whitespace)
        all_chars = set(string.printable)
        chars_to_use = list(all_chars - white_space_chars)
        chars_to_use = "".join(chars_to_use)
        self.current_layer = []
        self.to_pop = []
        self.config.char_bag = list(pg.PASSWORD_END + pg.PASSWORD_START + chars_to_use)
        self.root_node = tree.Node("", 1)
        self.passwords =[]
        sys.setrecursionlimit(50000)


        #TODO: REMOVE THIS. Its only to test the association Markov.
        self.assocation_pass = []
        self.char_pass = []
        # TODO: REMOVE THIS. Its only to test the association Markov.

        if initilize_here:
            self.m = Markov.MarkovModel(self.config, smoothing='none', order= self.char_markov_order)
            self.m.train(self.training_data)
            self.association_prediction_markov = Association_markov.Association_Prediction_Markov(self.max_pwd_len, self.training_data, self.association_rule_path, do_train=True)
            self.association_prediction_markov.train()
            #self.initialize_first_current_layer()




        else:
            self.m = None
            self.association_prediction_markov = None
        self.association_guesses = []



    def __iter__(self):
        return self

    def __next__(self):

        try:
            next_password = self.get_next()  # Next password might not be the complete guess
            if "\n" in next_password[0][1]:
                prob = next_password[0][0]
                formatted_password = next_password[0][1].strip()
                #print("from Iterator")
                return formatted_password
                # passwords.append((prob,formatted_password))
        except:
            raise StopIteration


    def set_values(self, training_data, source_char_markov_model, source_injection_markov_model, association_rules=None, association_rule_path=None):
        self.training_data = training_data
        self.association_rule_path = association_rule_path
        self.association_rules = association_rules

        #Create Local char Markov
        self.m = Markov.MarkovModel(self.config, smoothing='none', order=self.char_markov_order)
        self.m.freq_dict = source_char_markov_model.freq_dict
        self.m.config = source_char_markov_model.config
        self.m.alphabet = source_char_markov_model.alphabet
        self.m.configure_smoother()
        #self.m.train(self.training_data)


        self.association_prediction_markov = Association_markov.Association_Prediction_Markov(self.max_pwd_len, self.training_data, self.association_rule_path, do_train=False)
        self.association_prediction_markov.freq_dict = source_injection_markov_model.freq_dict
        #self.association_prediction_markov.config = source_injection_markov_model.config
        #self.association_prediction_markov.alphabet = source_injection_markov_model.alphabet
        self.current_layer = []
        self.to_pop = []
        self.initialize_first_current_layer()


    def create_new_models(self):
        char = Markov.MarkovModel(self.config, smoothing='none', order=self.char_markov_order)
        char.freq_dict = self.m.freq_dict
        char.config = self.m.config
        char.alphabet = self.m.alphabet
        char.configure_smoother()



        assoc = Association_markov.Association_Prediction_Markov(self.max_pwd_len, self.training_data, self.association_rule_path, do_train=False)
        assoc.freq_dict = self.association_prediction_markov.freq_dict


        return (char, assoc)


    #TODO: Should paswords used for training have the start and end characters?
    def generate_dataset_from_textfile(self,textfile_path):
        words_dict = {}
        list_to_return = []
        text_file = open(textfile_path,"r")
        for word in text_file:
            word = word.strip()
            if word in words_dict:
                words_dict[word] += 1
            else:
                words_dict[word] = 1

        for key,value in words_dict.items():
            list_to_return.append(("\t"+key,value))

        #print("list to return")
        #print(list_to_return)
        return list_to_return



    #print(generate_dataset_from_textfile("/Users/thomasbekman/Desktop/pass.txt"))

    #training_data = generate_dataset_from_textfile("/Users/thomasbekman/Documents/Research/Passwords/Cracked_Passwords/mySpace.txt")


    #training_data("/Users/thomasbekman/Documents/Research/Passwords/Cracked_Passwords/1.txt")


    #Call not needed if using the new scoring function
    #common_substrings = read_common_substrings_into_memory(200)
    #association_rules = mem_utils.read_association_rules_into_memory("/Users/thomasbekman/Documents/Research/SpadeFiles/MinSup20000,MinConf0.1_HalfData/Patterns_halfData.txt")
    #print("!!!!!!!!!")
    #print(association_rules)
    #print("!!!!!!!!!")

    def find_first_part_association_rules_for_string(self, password):
        assocation_rules_satisfied = []

        substrings = Utils.subStringFinder(password)


        for substring in substrings:
            if (substring in self.association_rules):
                for second_part_of_association in self.association_rules[substring].keys():
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
    def add_assocation_rules_to_prob(self, currentPassword,  char_to_add):
            association_prob = 0
            start_time = time.time()

            new_word = currentPassword + char_to_add

            assocation_rules_satisfied = self.find_first_part_association_rules_for_string(new_word)


            for rule in assocation_rules_satisfied:

                #If you want to make this more stringent, then you should add the following to the if block:  and rule[1]  not in currentPassword
                #This would only increase the probability when the association rule is created with the addition of the letter. Instead of now where the probabilties are increased for every letter added after the creation of an association rule.
                if(rule[0] in new_word and rule[1] in new_word):
                    first_string_end_position = new_word.find(rule[0]) + len(rule[0])-1 #The first word in the association rules
                    second_string_start_position = new_word.find(rule[1])

                    if(second_string_start_position > first_string_end_position):
                        association_prob = Scoring.association_rule_coverage(new_word)

            #print("Association check took", time.time() - start_time, "s to run")
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
    def add_common_substring_to_prob(self, currentPassword, char_to_add,  cutoff):
            substring_prob = 0

            start_time = time.time()

            new_word = currentPassword + char_to_add
            substring_prob = Scoring.common_substring_coverage(new_word, cutoff)
            #print("Substring Time:", time.time() - start_time, "s to run")

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

    def add_common_regex_to_prob(self, currentPassword, char_to_add):
        regex_prob = 0


        start_time = time.time()

        new_word = currentPassword + char_to_add
        new_word = new_word.strip()
        regex_prob = Scoring.regex_rulecoverage(new_word)
       # print("Regex Time:", time.time() - start_time, "s to run")

        return regex_prob


    #To Test common_regex
    '''
    print("test Regex_to_prob")
    start_time = time.time()
    #add_common_regex_to_prob("Pass0034",fake_prob_vector, 0.25, 0.2)
    print ("REGEX check took", time.time() - start_time, "s to run")
    '''


    def calculate_weighted_average(self, markov_prob, association_prob,  regex_prob, markov_weight, association_weight, regex_weight):

        total_weight = association_weight  + regex_weight + markov_weight
        markov_contribution = markov_prob * markov_weight
        association_contribution = association_prob * association_weight
        #substring_contribution = substring_prob * substring_weight
        regex_contribution = regex_prob * regex_weight
        weighted_average = (association_contribution + regex_contribution + markov_contribution) / total_weight
        return weighted_average

    '''
    Converts the probability vector into a char prediction dictionary.
    
    This was modified to also check if an association word should be added. 
    '''
    def probabilityToChar(self, charbag, probabilities, current_word):
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
    '''
    config = Mock()
    white_space_chars = set(string.whitespace)
    all_chars = b = set(string.printable)
    chars_to_use = list(all_chars - white_space_chars)
    chars_to_use = "".join(chars_to_use)


    config.char_bag = list(pg.PASSWORD_END +pg.PASSWORD_START + chars_to_use)
    m = Markov.MarkovModel(config, smoothing='none', order=4)
    #m.train([('\tpass+A', 5), ('\tpast', 1), ('\tashen', 1), ('\tas&^R$s', 1), ('\tbl+ah', 1),('\tbl+ahs', 1),('\tblhma', 1), ('\tblmag', 1)])
    m.train(training_data)
    

    print(m.freq_dict)
    #answer = np.zeros((len(config.char_bag), ), dtype=np.float64)
    #m.predict('', answer)

    #probabilityToChar(config.char_bag, {}, "c123")
    '''
    def pop_max(self, input_list):
        list1 = [input_list.pop(input_list.index(max(input_list)))]
        return list1

    '''
    Initalize first layer creates the first layer you want for you markov tree. 
    It currently starts creating string from the empty string
    '''

    #The two vars below are used in the getNext function
    #current_layer = []
    #to_pop = []
    def initialize_first_current_layer(self):
        answer = np.zeros((len(self.config.char_bag),), dtype=np.float64)
        a= self.m
        self.m.predict("", answer)
        prediction_dict = self.probabilityToChar(self.m.alphabet, answer, "")


        for key in prediction_dict.keys():
            self.current_layer.append((prediction_dict[key],key))
    '''
    Calling this function returns you the next prediction. 
    '''
    #TODO: The current method creates a lot of duplicates
    #association_prediction_markov = Association_markov.Association_Prediction_Markov(10,training_data,"/Users/thomasbekman/Documents/Research/SpadeFiles/MinSup20000,MinConf0.1_HalfData/Patterns_halfData.txt")
    #association_guesses = []



    def get_next(self):
        if self.to_pop != []:
            return self.pop_max(self.to_pop)
        else:
            new_current = []
            for substring in self.current_layer:
                answer = np.zeros((len(self.config.char_bag)), dtype=np.float64)
                #if not any(substring in word for word in to_pop):   An initial attempt to remove duplicates, but it doesn't really work as the two markov models arrive at the same conclusions independently
                self.to_pop.append(substring)
                self.m.predict(substring[1], answer)
                association_predictions = self.association_prediction_markov.predict(substring[1])




                #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                #To test uniqueness of association
                '''

                #print("I'm the charbag")
                #print( self.association_prediction_markov.charbag)
                #print("I'm the charbag")
                '''
                '''
                answer_1 = np.zeros((len(self.config.char_bag)), dtype=np.float64)

                self.m.predict(substring[1], answer_1)
                char_probs_1 = self.probabilityToChar(self.m.alphabet, answer_1, substring)


                for prob in char_probs_1:
                    pass_made = substring[1] + prob[0]

                    #if "\n" in pass_made:
                    self.char_pass.append(pass_made)

                for prob in association_predictions:
                    pass_made = substring[1] + prob[0]

                    #if "\n" in pass_made:
                    self.assocation_pass.append(pass_made)
            
                '''




                # To test uniqueness of association
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!








                #prediction_dict = self.probabilityToChar(self.m.alphabet, answer, substring)
                prediction_dict = {**self.probabilityToChar(self.m.alphabet, answer, substring), **association_predictions}
                for prediction in prediction_dict.items():
                    to_add_word = substring[1] + prediction[0]
                    markov_prob = prediction[1]
                    #The substring weighting was seen as redundant and removed.
                    #substring_prob = add_common_substring_to_prob(substring[1], prediction[0],  100000)  # Adds substring probabilities

                    #TODO: Speed these up. BIG PROBLEM
                    association_prob = 0#self.add_assocation_rules_to_prob(substring[1], prediction[0])
                    regex_prob = 0#self.add_common_regex_to_prob(substring[1], prediction[0])

                    weighted_average_probs = self.calculate_weighted_average(markov_prob, association_prob ,regex_prob , 1, 0, 0) #TODO: Update this so it is no longer hard coded
                    to_add_prob = substring[0] * weighted_average_probs #Mulitplies the current probability with that of the parent
                    if ((len(to_add_word) <= self.max_pwd_len +2)): #Because the start and end chars each have an extra char. So 2 extra total by traditional python string length counting
                        #if not any(to_add_word in  word for word in new_current): SAME ATTEMPT AT removing duplicates as shown above
                        new_current.append((to_add_prob,to_add_word))
        self.current_layer = new_current
        return self.pop_max(self.to_pop)


    #TODO: This probably needs to write to the mongoDB, or batch write a text file. All passwords should probably be made before the testing stage.
    #TODO: REMOVE THIS COMMENT LATER
    #initialize_first_current_layer()
    def generatePasswords(self):
        passwords = []
        #print("ran once")
        '''
        next_password = get_next(7)  # Next password might not be the complete guess
        if "\n" in next_password[0][1]:
            prob = next_password[0][0]
            formatted_password = next_password[0][1]
            passwords.append((prob, formatted_password))
        '''
        try:
            while True:
                next_password = self.get_next() #Next password might not be the complete guess
                if "\n" in next_password[0][1]:
                    prob = next_password[0][0]
                    formatted_password = next_password[0][1].strip()
                    yield formatted_password
                    #passwords.append((prob,formatted_password))
        except:
            for i in passwords:
                print(i)
            #return passwords


    #Test of old method



    def markovBuilder(self, currentNode, maxPasswordLength=4):
        config = Mock()


        #config.char_bag = pg.PASSWORD_END + 'abcdefghiklmnopqrst' + pg.PASSWORD_START + "ABCDEFGHIJKLMNOPQRSTRUV"
        answer = np.zeros((len(self.config.char_bag),), dtype=np.float64)
        if ("\n" not in currentNode.value and len(currentNode.value) <= maxPasswordLength):
            # m.predict(currentNode.value, answer)
            # char_to_add = probabilityToChar(m.alphabet, answer)
            self.m.predict(currentNode.value, answer)
            association_predictions = self.association_prediction_markov.predict(currentNode.value)

            prediction_dict = {**self.probabilityToChar(self.m.alphabet, answer, currentNode.value), **association_predictions}
            #prediction_dict = self.probabilityToChar(self.m.alphabet, answer, currentNode.value)
            predict_items = prediction_dict.items()
            #print(prediction_dict)

            #prediction_dict = self.probabilityToChar(self.m.alphabet, answer, currentNode.value)
            for char, probability in predict_items:

                newString = currentNode.value + char
                newProbability = probability * currentNode.priority  # Multiplies the current probability with the parents. This way all the probabilties used to generate each string are taken into account
                #print(newString)
                new_node_to_add = tree.Node(newString, newProbability)
                currentNode.add_child(new_node_to_add)

            #currentNode.value = None
            #currentNode.priority = None

            #TODO: make the call without the sorting, this is really slowing thrings down!!!
            #for child in currentNode.getChildren():
            for child in  currentNode.children:
                self.markovBuilder(child)


    def getPasswords(self):
        print("Size of the markov builder")

        self.markovBuilder(self.root_node)


        def getPasswords_1(node):
            if (node.getChildren() != []):
                for sibling in node.getChildren():
                   getPasswords_1(sibling)
            else:
                if(node.value is not None):
                    if("\n" in node.value):
                        self.passwords.append(node.value)

        getPasswords_1(self.root_node)

        print("!!!!!")
        #print(self.passwords)


    def predict_next_substring(self,char, assoc, current_value, current_priority,  use_assocation_rules=False):
        #Format: [(prob, string), (prob,string) ...]
        new_predictions = []

        answer = np.zeros((len(self.config.char_bag),), dtype=np.float64)
        char.predict(current_value, answer)


        if use_assocation_rules:
            association_predictions = assoc.predict(current_value)

            prediction_dict = {**self.probabilityToChar(char.alphabet, answer, current_value),
                           **association_predictions}


        #Case with no association rules
        else:
            prediction_dict = self.probabilityToChar(char.alphabet, answer, current_value)


        predict_items = prediction_dict.items()
        for char, probability in predict_items:
            newString = current_value + char
            newProbability = probability * current_priority
            new_predictions.append((newProbability, newString))
        return new_predictions

    #def predict_next_substring_non_dsitributed(self,char, assoc, current_value, current_priority,  use_assocation_rules=False):
    def predict_next_substring_non_dsitributed(self, current_value, current_priority, use_assocation_rules=False):
        # Format: [(prob, string), (prob,string) ...]
        new_predictions = []

        answer = np.zeros((len(self.config.char_bag),), dtype=np.float64)
        self.m.predict(current_value, answer)

        if use_assocation_rules:
            association_predictions = self.association_prediction_markov.predict(current_value)

            prediction_dict = {**self.probabilityToChar(self.m.alphabet, answer, current_value),
                               **association_predictions}


        # Case with no association rules
        else:
            prediction_dict = self.probabilityToChar(self.m.alphabet, answer, current_value)

        predict_items = prediction_dict.items()
        for char, probability in predict_items:
            newString = current_value + char
            newProbability = probability * current_priority
            new_predictions.append((newProbability, newString))
        return new_predictions

    # non-recursive approach, with minimal memory overhead. Needs to be sorted in the end.
    def get_passwords_no_recusion_non_distributed(self, start_point, max_pwd_length=4):

        count_1 =0
        completed_passwords = []
        to_work = self.predict_next_substring_non_dsitributed(start_point, 1, True)
        next =[]
        while to_work != []:
            for node in to_work:
                next_string = node[1]
                next_prob = node[0]
                next_prediction = self.predict_next_substring_non_dsitributed(next_string, next_prob, True)
                for i in next_prediction:
                    next.append(i)
                    #if (len(i[1]) - 1 <= max_pwd_length):
                    #    next.append(i)
            #print(to_work)
            to_work.clear()
            meh =0
            for node in next:
                next_string = node[1]
                next_prob = node[0]
                #IS IT? #BROKEN HERE
                if (next_string[-1:] == "\n" ):#and len(next_string)-2 <= max_pwd_length):
                    #print("sadasdas")
                    #print(next_string[-1:])
                    a = next_string[-1:]
                    #print("sadasdas")

                    completed_passwords.append(next_string)
                    #count_1 += 1
                    #meh = count_1 / 25000 * 100
                    #print(str((count_1 / 25000) * 100) + "%")

                else:
                    #a =None
                    #b = None
                    next_prediction = self.predict_next_substring_non_dsitributed(next_string, next_prob, True)
                    for i in next_prediction:
                        #if meh > 19.84:
                        #    print(len(next_prediction))

                        if(i[1][-1:] == "\n"):
                            completed_passwords.append(i[1])

                        elif(len(i[1])-2 <= max_pwd_length):
                            to_work.append(i)

                    #count = len(to_work)
                    '''
                    for prob,string in to_work:
                        if(len(string)>max_pwd_length):
                            count -= 1
                    if count ==0:
                         pass
                         break

                    '''


            #print(next)
            next.clear()

        #print(completed_passwords)
        return completed_passwords



    # non-recursive approach, with minimal memory overhead. Needs to be sorted in the end.
    def get_passwords_no_recursion(self, char, assoc, start_point, max_pwd_length=4):

        count_1 =0
        completed_passwords = []
        to_work = self.predict_next_substring(char,assoc,start_point, 1, True)
        next =[]
        while to_work != []:
            for node in to_work:
                next_string = node[1]
                next_prob = node[0]
                next_prediction = self.predict_next_substring(char, assoc, next_string, next_prob, True)
                for i in next_prediction:
                    next.append(i)
                    #if (len(i[1]) - 1 <= max_pwd_length):
                    #    next.append(i)
            #print(to_work)
            to_work.clear()
            meh =0
            for node in next:
                next_string = node[1]
                next_prob = node[0]
                #IS IT? #BROKEN HERE
                if (next_string[-1:] == "\n" ):#and len(next_string)-2 <= max_pwd_length):
                    #print("sadasdas")
                    #print(next_string[-1:])
                    a = next_string[-1:]
                    #print("sadasdas")

                    completed_passwords.append(next_string)
                    #count_1 += 1
                    #meh = count_1 / 25000 * 100
                    #print(str((count_1 / 25000) * 100) + "%")

                else:
                    #a =None
                    #b = None
                    next_prediction = self.predict_next_substring(char, assoc, next_string, next_prob, True)
                    for i in next_prediction:
                        #if meh > 19.84:
                        #    print(len(next_prediction))

                        if(i[1][-1:] == "\n"):
                            completed_passwords.append(i[1])

                        elif(len(i[1])-2 <= max_pwd_length):
                            to_work.append(i)

            #print(next)
            next.clear()

        #print(completed_passwords)



    def combine_generated_passwords(self):
        text_files = glob.glob("generated_password_store/*.txt")
        training_data = []
        for file in text_files:
            with open(file) as text_file:
                list_from_disk = json.loads(text_file.read())
                training_data = training_data + list_from_disk

        #TODO: FINSIH ME





    def distributed_generate_passwords(self):


        char_first, assoc_first =  self.create_new_models()

        #self.predict_next_substring(char, assoc, next_string, next_prob, True)

        first_layer_nodes = self.predict_next_substring(char_first, assoc_first, "\t", 1, True)

        first_layer = []

        for node in first_layer_nodes:
            first_layer.append(node[1])

        args = []

        start = time.time()
        for i in range(len(first_layer)):
            char, assoc = self.create_new_models()

            args.append((char,assoc,first_layer[i]))

        end = time.time()
        print("Time to make models")
        print(end-start)

        #print([char_models, assoc_models, first_layer])

        with Pool(multiprocessing.cpu_count()) as p:
            # results = p.map(find_number_guesses, passwords)

            p.starmap(self.get_passwords_no_recursion, args)
            #p.map(self.get_passwords_no_recursion, first_layer)


        #return passwords




'''
print("----")
print(generatePasswords())
print("----")
'''




'''
print("Starting test below")




#a = Association_markov.Association_Prediction_Markov(5)
a = Association_markov.Association_Prediction_Markov(8,training_data,"/Users/thomasbekman/Documents/Research/SpadeFiles/MinSup20000,MinConf0.1_HalfData/Patterns_halfData.txt")
print("/////")
print(a.predict("\t3456712"))
print("/////")

#ab= Association_Predicting_Markov_2.test()
#a = Association_Predicting_Markov_2.Association_Prediction_Markov()
#a.update_charbag("1234567")
#print(a.charbag)

#a = Markov_Attempt.Association_Predicting_Markov.PASSWORD_START





print("Starting large scale test")
start_time = time.time()




'''

'''
print("!!!!")
a = Association_markov.Association_Prediction_Markov(8,training_data,"/Users/thomasbekman/Documents/Research/SpadeFiles/MinSup20000,MinConf0.1_HalfData/Patterns_halfData.txt")

c = a.freq_dict

#answer = a.predict("s34a")
#charbag, probabilities, current_word
#print("Guess s34a" + str(probabilityToChar(a.charbag,answer,"Irrelavant arg")))

#answer = a.predict("567")
#charbag, probabilities, current_word
#print("Guess 567" + str(probabilityToChar(a.charbag,answer,"Irrelavant arg")))

answer = a.predict("567a")
#charbag, probabilities, current_word
#print("Guess 567" + str(probabilityToChar(a.charbag,answer,"Irrelavant arg")))


answer = a.predict("567b")
#charbag, probabilities, current_word
#print("Guess 567" + str(probabilityToChar(a.charbag,answer,"Irrelavant arg")))

answer = a.predict("\tv")
#charbag, probabilities, current_word
#print("Guess 567" + str(probabilityToChar(a.charbag,answer,"Irrelavant arg")))

answer = a.predict("567d")
'''
#charbag, probabilities, current_word
'''
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



a = Association_markov.Association_Prediction_Markov(8,training_data,"/Users/thomasbekman/Documents/Research/SpadeFiles/MinSup20000,MinConf0.1_HalfData/Patterns_halfData.txt")
answer = a.predict("3456")
#charbag, probabilities, current_word
print("Guess 34" + str(answer))

'''

'''
class Create_Password_Guesses:
    def __init__(self, training_data_path, association_rule_path, char_markov_order, char_assocation_order, max_pwd_len):
'''
#Markov_Attempt.Runner.Create_Password_Guesses("/Users/thomasbekman/Documents/Research/Passwords/Cracked_Passwords/1.txt", "/Users/thomasbekman/Documents/Research/SpadeFiles/MinSup20000,MinConf0.1_HalfData/Patterns_halfData.txt", 4, 8, 11)
#'''
'''
for i in Create_Password_Guesses("/Users/thomasbekman/Documents/Research/Passwords/Cracked_Passwords/1.txt", "/Users/thomasbekman/Documents/Research/SpadeFiles/MinSup20000,MinConf0.1_HalfData/Patterns_halfData.txt", 4, 8, 11):
    print("From loop")
    print(i)
'''
'''
tom =Create_Password_Guesses(
"/Users/thomasbekman/Documents/Research/Passwords/Cracked_Passwords/Use_me.txt",
"/Users/thomasbekman/Documents/Research/SpadeFiles/MinSup20000,MinConf0.1_HalfData/Patterns_halfData.txt", 4, 8,
11)
'''


'''
for i in tom.generatePasswords():
    print(i)

'''


#Newly attempted Markov Building code
'''

'''

