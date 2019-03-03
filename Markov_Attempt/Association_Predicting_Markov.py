import Markov_Attempt.Markov as Markov
import collections
from unittest.mock import Mock, MagicMock
import string
import Password_Sorting.Utils as Utils
import Markov_Attempt.pwd_guess as pg
import Markov_Attempt.Utils as Mem_utils
import numpy as np



class Association_Prediction_Markov():
    def __init__(self, max_password_length, training_data, association_rule_path):
        self.freq_dict = collections.defaultdict(int)
        self.charbag = []
        self.association_rules = Mem_utils.read_association_rules_into_memory(association_rule_path)


        #Now we create a massive freq dict with all the order from 2 to max. This is necessary for predictions.

        config = Mock()
        config.char_bag = ["\n", "\t"] #This value doesn't matter, its just a fake value given to intitialize markov models below

        for i in range(2, max_password_length+1):
            m = Markov.MarkovModel(config, smoothing='none', order=i)
            m.train(training_data)
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


    def predict(self, password):
        self.update_charbag(password)

        config = Mock()
        config.char_bag = self.charbag
        answer = np.zeros((len(self.charbag)), dtype=np.float64)
        m = Markov.MarkovModel(config, order=3) #We are using this to make predictions. For predictions order does not matter
        m.freq_dict = self.freq_dict
        m.configure_smoother()
        m.predict(password,answer,False)
        return answer





#This needs to be on the bottom due to cyclic import with Runner.py
