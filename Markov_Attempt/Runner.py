import Markov_Attempt.Markov as Markov
import Markov_Attempt.pwd_guess as pg
from multiprocessing import Pool
import multiprocessing
import glob
import json
import struct
import hashlib
from unittest.mock import Mock, MagicMock
import numpy as np
import sys
import time
#import Password_Sorting.Password_Scoring as Scoring
import string
import math
import Password_Sorting.Utils as Utils
import Markov_Attempt.Association_Predicting_Markov as Association_markov
import Markov_Attempt.Utils as mem_utils
import collections
import Markov_Attempt.treeForMarkov as tree
from operator import itemgetter
from collections import deque
import Markov_Attempt.Configuration_Values
import os
class config_mock():
    def __init__(self):
        self.charbag = []



class Create_Password_Guesses():

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


        #THis if/else might be worthless, but removing it would force me to refactor :(
        if initilize_here:
            self.m = Markov.MarkovModel(self.config, smoothing='none', order= self.char_markov_order)
            self.m.train(self.training_data)
            self.association_prediction_markov = Association_markov.Association_Prediction_Markov(self.max_pwd_len, self.training_data, self.association_rule_path, do_train=True)
            self.association_prediction_markov.train()


        else:
            self.m = None
            self.association_prediction_markov = None
        self.association_guesses = []


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

        for i in enumerate(probabilities):
            if i[1] > Markov_Attempt.Configuration_Values.probability_cutoff and i[1] != math.inf and not np.isnan(i[1]):
                char_probs[charbag[i[0]]] = i[1]
        return char_probs


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
                    if (len(i[1]) - 2 <= max_pwd_length):
                        next.append(i)
            #print(to_work)
            to_work.clear()
            meh =0
            for node in next:
                next_string = node[1]
                next_prob = node[0]
                #IS IT? #BROKEN HERE
                print("TEST: " + next_string)
                if (next_string[-1:] == "\n" and len(next_string)-2 <= max_pwd_length):#and len(next_string)-2 <= max_pwd_length):
                    #print("sadasdas")
                    #print(next_string[-1:])
                    a = next_string[-1:]
                    #print("sadasdas")
                    print("1: "  + next_string)
                    completed_passwords.append((next_prob,next_string))
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

                        if(i[1][-1:] == "\n"and len(i[1])-2 <= max_pwd_length):
                            print("1" + i[1])

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
    def get_passwords_no_recursion(self, char, assoc, start_point, start_prob, max_pwd_length=10):
        start = time.time()
        total = 0
        completed_passwords = []
        to_work = self.predict_next_substring(char,assoc,start_point, start_prob, True)
        print("started: " + str(os.getpid()))
        next =[]
        while to_work != []:

            for node in to_work:
                next_string = node[1]
                next_prob = node[0]
                next_prediction = self.predict_next_substring(char, assoc, next_string, next_prob, True)

                for i in next_prediction:


                    if (i[1][-1:] == "\n" and len(i[1]) - 2 <= max_pwd_length):
                        total += 1
                        completed_passwords.append((next_prob,next_string))
                        if total > Markov_Attempt.Configuration_Values.number_passwords_to_make:
                            with open("generated_password_store/" + str(start_point.strip()) + ".txt", "w+") as file:
                                file.write(json.dumps(completed_passwords))
                            end = time.time()
                            print("Done: " + str(os.getpid()) + " " + str(end - start) + "s")
                            return


                    elif (len(i[1]) - 2 <= max_pwd_length):
                        next.append(i)


            to_work.clear()
            for node in next:
                next_string = node[1]
                next_prob = node[0]

                next_prediction = self.predict_next_substring(char, assoc, next_string, next_prob, True)

                for i in next_prediction:

                    if(i[1][-1:] == "\n" and len(i[1])-2 <= max_pwd_length):
                        total += 1
                        completed_passwords.append((next_prob, next_string))
                        if total > Markov_Attempt.Configuration_Values.number_passwords_to_make:
                            with open("generated_password_store/" + str(start_point.strip()) + ".txt", "w+") as file:
                                file.write(json.dumps(completed_passwords))
                            end = time.time()
                            print("Done: " + str(os.getpid()) + " " +str(end-start)+"s")
                            return



                    elif(len(i[1])-2 <= max_pwd_length):
                        to_work.append(i)



            #print("TO WORK\n\n\n" )
            #print(len(to_work))

            next.clear()



        #print(completed_passwords)



    def combine_generated_passwords(self):
        text_files = glob.glob("generated_password_store/*.txt")
        training_data = []
        for file in text_files:
            with open(file) as text_file:
                list_from_disk = json.loads(text_file.read())
                #print(list_from_disk)
                # TODO: Modify this. For the sake of temporary testing this is fine. But needs to be updated for the full dataset. n
                training_data = training_data + list_from_disk


        #TODO: Remove this redundant step later on with larger datasets.
        with open("unsorted_passwords.txt", "w+") as file:
            file.write(json.dumps(training_data))


    def get_pass_hash(self, password):
        arr = bytes(password, 'utf-8')
        hash = hashlib.md5(arr).digest()
        num = int.from_bytes(hash,"little")
        string_num = str(num)
        return string_num



    def write_passwords_to_disk(self, passwords, number_of_files):


        for i in passwords:
            file_name = self.get_pass_hash(i[1])
            file_name_final = file_name[-number_of_files:]+".txt"


            with open("final_formatted_password_store/"+file_name_final, "a") as file:
                file.write(json.dumps(i) + "\n")

    def sort_generated_passwords(self):
        with open("unsorted_passwords.txt", "r") as text_file:
             to_sort = json.loads(text_file.read())

        to_sort.sort(key=itemgetter(0), reverse = True)

        #with open("sorted_passwords_1.txt", "w")as text_file:
        #    text_file.write(json.dumps(to_sort))


        for i in range(0,len(to_sort)):
            to_sort[i][0] = i+1

        self.write_passwords_to_disk(to_sort,2)



    def distributed_generate_passwords(self):


        char_first, assoc_first =  self.create_new_models()

        #self.predict_next_substring(char, assoc, next_string, next_prob, True)

        #first_layer_nodes = self.predict_next_substring(char_first, assoc_first, "\t", 1, False)
        import string
        first_layer = []
        #FIRST LAYER OF TREE
        white_space_chars = set(string.whitespace)
        all_chars = set(string.printable)
        chars_to_use = list(all_chars - white_space_chars)
        chars_to_use = "".join(chars_to_use)
        for string in chars_to_use:
            first_layer.append("\t"+string)
        '''
        # (prob,word)
        next_layer = []
        #SECOND LAYER OF TREE
        for prob, password in first_layer_nodes:

            predictions = self.predict_next_substring(char_first, assoc_first, password, prob, True)
            for prediction in predictions:
                next_layer.append(prediction)


        first_layer.clear()

        #THIRD LAYER OF TREE
        for prob, password in next_layer:
            predictions = self.predict_next_substring(char_first, assoc_first, password, prob, True)
            for prediction in predictions:
                first_layer.append(prediction)

        #First layer now actually has up to the third layer of the tree
        next_layer.clear()
        '''
        args = []

        start = time.time()
        for i in first_layer:
            char, assoc = self.create_new_models()
            # char, assoc, start_point, start_prob,
            prob = 1
            password = i
            args.append((char,assoc,password,prob))

        end = time.time()
        print("Time to make models")
        print(end-start)

        #print([char_models, assoc_models, first_layer])

        start = time.time()
        #Used to be multiprocessing.cpu_count(). Was dropped to 12 due to excessive RAM usage
        #print(args)
        with Pool(multiprocessing.cpu_count()) as p:
            # results = p.map(find_number_guesses, passwords)

            p.starmap(self.get_passwords_no_recursion, args)
            #p.map(self.get_passwords_no_recursion, first_layer)
        end = time.time()
        print("Time produce passwords")
        print(end - start)

        print("Time to merge passwords files")
        start = time.time()
        self.combine_generated_passwords()
        end = time.time()
        print(end - start)

        print("Time to sort passwords, and rewrite them to disk")
        start = time.time()
        self.sort_generated_passwords()
        end = time.time()
        print(end - start)
