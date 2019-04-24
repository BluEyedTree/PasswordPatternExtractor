from multiprocessing.pool import ThreadPool
import multiprocessing
import Markov_Attempt.Runner
import Markov_Attempt.Runner
import time
import copy
Markov_Attempt.Runner
Runner =  Markov_Attempt.Runner
maximum_password_length = 14




'''
print("test")
for i in Runner.generatePasswords():
    print(i)
print("test")
'''

###
#Create the Markov Objects that will be used for creating guesses for all the threads.

#def set_values(self, #training_data, #source_char_markov_model, #source_injection_markov_model, association_rules=None, association_rule_path=None, char_markov_order=None, char_assocation_order=None, max_pwd_len=None, chars_to_use_in=None):

markov_obj = Markov_Attempt.Runner.Create_Password_Guesses(initilize_here=True,
    training_data_path= "/Users/thomasbekman/Documents/Research/Passwords/Cracked_Passwords/1.txt",
    association_rule_path= "/Users/thomasbekman/Documents/Research/SpadeFiles/MinSup20000,MinConf0.1_HalfData/Patterns_halfData.txt", char_markov_order=4, char_assocation_order=8, max_pwd_len=11)

training_data = markov_obj.training_data
char_markov_model = markov_obj.m
association_markov_model = markov_obj.association_prediction_markov
association_rules = markov_obj.association_rules
association_rule_path = markov_obj.association_rule_path




def find_number_guesses(password):
    count = 0
    print("-------")
    print("state 2")
    markov_obj_meh = Markov_Attempt.Runner.Create_Password_Guesses(initilize_here=False, char_markov_order=4, char_assocation_order=8, max_pwd_len=11)
    markov_obj_meh.set_values(training_data, char_markov_model, association_markov_model, association_rules, association_rule_path)


    try:
        print("state 3")
        for get_next_password in markov_obj_meh:
            print("state4")
            #print("Yes_Man")

            if (get_next_password != None):
                count += 1
            if(get_next_password != None and get_next_password == password):
                print("password")
                print(password)
                print("password_guess")
                print(get_next_password)
                return (count,password)
        print("-------")
    except:
        print("failure")
        pass


# function to be mapped over
def calculateParallel(passwords, threads=1):   #Thread number should really be: threads=multiprocessing.cpu_count()
    pool = ThreadPool(threads)
    results = pool.map(find_number_guesses, passwords)
    pool.close()
    pool.join()
    return results


def run_grading(test_dataset_path):
    #test_data is a set of passwords
    test_data = [] #This should be fine as long as the test dataset is under 10 billion on the lab server (that would be approx 190GB)
    with open(test_dataset_path) as f:
        for line in f:
            print("1")
            print(line)
            test_data.append(line.strip())

    #guesses = calculateParallel(test_data)
    tom = find_number_guesses("r23e123er23")
    print(tom)
    '''
    for n in guesses:
        #print("new_test")
        #print(n)
        blah = n
        pass
    '''

start = time. time()



run_grading("/Users/thomasbekman/Documents/Research/Passwords/test_passwords/grading_test.txt")
end = time. time()
print("TIME IT TOOK")
print(end - start)