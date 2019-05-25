import Markov_Attempt.Markov as Markov
from multiprocessing import Pool
import collections
from unittest.mock import Mock, MagicMock
import string
import Password_Sorting.Utils as Utils
import Markov_Attempt.pwd_guess as pg
import Markov_Attempt.Utils as Mem_utils
import numpy as np
import math
from multiprocessing import Process, Manager
import json
import glob



class Association_Prediction_Markov():
    def __init__(self, max_password_length, training_data, association_rule_path, do_train=False):
        self.training_data = training_data
        self.max_password_length = max_password_length
        self.freq_dict = collections.defaultdict(int)
        self.charbag = []
        self.association_rules = Mem_utils.read_association_rules_into_memory(association_rule_path)

    def train_Model(self, order):
        dict = self.train_markovModel(self.training_data,order)
        with open("text_store/" + str(order)+".txt", "w+") as file:
           file.write(json.dumps(dict))
        print("order " + str(order) +"Done")
        return 0

    def Merge(self, dict1, dict2):
        res = {**dict1, **dict2}
        return res

    def combine_json_textfiles(self):
        text_files = glob.glob("text_store/*.txt")
        training_data = {}
        for file in text_files:
            with open(file) as text_file:
                dict_to_add = json.loads(text_file.read())
                training_data = self.Merge(training_data, dict_to_add)

        self.freq_dict = training_data





    def train(self):

        # A multiprocess approach to training each markov model.
        # We create a markov model for each order (from 2 to maxPassLength-1) then combine all their freq_dicts
        orders = []
        for i in range(2, self.max_password_length + 1):
            orders.append(i)


        with Pool(15) as p:
            # results = p.map(find_number_guesses, passwords)
            p.map(self.train_Model, orders)


        print("sdasdasdasd")
        self.combine_json_textfiles()


    '''
    Creates the freq dict of all different order markov models
    '''

    '''
    def create_composite_freq_dict(self):
        # Non-Parallel approach for debugging
        config = Mock()
        config.char_bag = ["\n", "\t"]
        for i in range(2, self.max_password_length + 1):
            m = Markov.MarkovModel(config, smoothing='none', order=i)
            m.train(self.training_data)
            print("Finished training for order " + str(i))
            self.freq_dict = {**self.freq_dict, **m.freq_dict}

        print(self.freq_dict)

    '''


   


        #print("-----")
        #print(self.freq_dict)
        #print("-----")




    #TODO: FIgure out how to make dics work, so you don't have to spend time joining lists later.
    def train_markovModel(self, training_data,  order):
        config = Mock()
        config.char_bag = ["\n", "\t"] #This value doesn't matter, its just a fake value given to intitialize markov models below
        m = Markov.MarkovModel(config, smoothing='none', order=order)
        m.train(training_data)
        #dict_to_write_to.append(m.freq_dict)
        return m.freq_dict


    '''
    The charbag is updated for every password. 
    If the first part of the association rule is present, then the charbag will contain the second part of the association
    '''
    def update_charbag(self, password):
        self.charbag = []
        seen = set()

        substrings = Utils.subStringFinder(password)
        for substring in substrings:
            if substring in self.association_rules:
                for second_part_of_association_rule in self.association_rules[substring].keys():

                    if second_part_of_association_rule not in password: #We dont want to double up on adding the second part of association rules.
                        if second_part_of_association_rule not in seen:
                            self.charbag.append(second_part_of_association_rule)
                            seen.add(second_part_of_association_rule)

                    if second_part_of_association_rule in password: #Deals with the case where the second part of the association is present, but exists before the first part. So its not a true association rule.
                        first_string_end_position = password.find(substring[0]) + len(substring[0]) - 1
                        second_string_start_position = password.rfind(second_part_of_association_rule)

                        if (second_string_start_position < first_string_end_position): #Second part occurs before the first.
                            if second_part_of_association_rule not in seen:
                                self.charbag.append(second_part_of_association_rule)
                                seen.add(second_part_of_association_rule)
        self.charbag = sorted(self.charbag)

    def probabilityToChar(self, probabilities):
        char_probs = {}

        for i in enumerate(probabilities):
            if i[1] != 0 and i[1] != math.inf and not np.isnan(i[1]):
                char_probs[self.charbag[i[0]]] = i[1]
        return char_probs



    def predict(self, password):
        self.update_charbag(password)
        if(self.charbag == []):
            return {}

        len_shortest_string_in_charbag = len(min(self.charbag, key=len))

        config = Mock()
        config.char_bag = self.charbag

        answer_prob_dict = {}
        for i in range(0, len(self.charbag)):
            answer_prob_dict[i] = 0

        for order_num in range(len_shortest_string_in_charbag+1, self.max_password_length):
            answer = np.zeros((len(self.charbag)), dtype=np.float64)
            m = Markov.MarkovModel(config, order=order_num) #We are using this to make predictions. For predictions order does not matter
            m.freq_dict = self.freq_dict
            m.configure_smoother()
            m.predict(password,answer,order_num)

            for i in enumerate(answer):

                if i[1] > answer_prob_dict[i[0]]:
                    answer_prob_dict[i[0]] = i[1]

            answer_to_return = np.zeros((len(self.charbag)), dtype=np.float64)
            for i in range(0, len(answer_to_return)):
                answer_to_return[i] = answer_prob_dict[i]


        return self.probabilityToChar(answer_to_return)

#This needs to be on the bottom due to cyclic import with Runner.py
