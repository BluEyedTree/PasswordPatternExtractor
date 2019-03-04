import Markov_Attempt.Markov as Markov
import collections
from unittest.mock import Mock, MagicMock
import string
import Password_Sorting.Utils as Utils
import Markov_Attempt.pwd_guess as pg
import Markov_Attempt.Utils as Mem_utils
import numpy as np
import math



class Association_Prediction_Markov():
    def __init__(self, max_password_length, training_data, association_rule_path):
        self.max_password_length = max_password_length
        self.freq_dict = collections.defaultdict(int)
        self.charbag = []
        self.association_rules = Mem_utils.read_association_rules_into_memory(association_rule_path)


        #Now we create a massive freq dict with all the order from 2 to max. This is necessary for predictions.

        config = Mock()
        config.char_bag = ["\n", "\t"] #This value doesn't matter, its just a fake value given to intitialize markov models below

        print("I'm the training data")
        print(training_data)
        print("I'm the training data")

        for i in range(2, max_password_length+1):
            m = Markov.MarkovModel(config, smoothing='none', order=i)
            m.train(training_data)
            print("Finished training for order "+str(i))
            self.freq_dict = {**self.freq_dict, **m.freq_dict}


        print(self.freq_dict)

    '''
    The charbag is updated for every password. 
    If the first part of the association rule is present, then the charbag will contain the second part of the association
    '''
    def update_charbag(self, password):
        self.charbag = []
        substrings = Utils.subStringFinder(password)
        for substring in substrings:
            if substring in self.association_rules:
                for second_part_of_association_rule in self.association_rules[substring].keys():
                    self.charbag.append(second_part_of_association_rule)

    def probabilityToChar(self, probabilities):
        char_probs = {}

        for i in enumerate(probabilities):
            if i[1] != 0 and i[1] != math.inf and not np.isnan(i[1]):
                char_probs[self.charbag[i[0]]] = i[1]
        return char_probs

    def predict(self, password):
        self.update_charbag(password)

        config = Mock()
        config.char_bag = self.charbag

        answer_prob_dict = {}
        for i in range(0, len(self.charbag)+1):
            answer_prob_dict[i] = 0


        for order_num in range(2, self.max_password_length):
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
