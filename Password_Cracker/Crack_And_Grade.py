import os
import psutil
from multiprocessing.pool import Pool
import multiprocessing
import Markov_Attempt.Runner
import Markov_Attempt.Runner
import time
import json
from multiprocessing import Pool

import os
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

'''
markov_obj = Markov_Attempt.Runner.Create_Password_Guesses(initilize_here=True,
    training_data_path= "/Users/thomasbekman/Documents/Research/Passwords/Cracked_Passwords/100k.txt",
    association_rule_path= "/Users/thomasbekman/Documents/Research/SpadeFiles/MinSup20000,MinConf0.1_HalfData/Patterns_halfData.txt", char_markov_order=4, char_assocation_order=8, max_pwd_len=11)

training_data = markov_obj.training_data
char_markov_model = markov_obj.m
association_markov_model = markov_obj.association_prediction_markov
association_rules = markov_obj.association_rules
association_rule_path = markov_obj.association_rule_path
print(training_data)
print("blah")
'''

''''''
def find_number_guesses(password):
    iteration_num =0

    print(os.getpid())

    count = 0
    print("-------")
    print("state 2")
    markov_obj_meh = Markov_Attempt.Runner.Create_Password_Guesses(initilize_here=False, char_markov_order=4, char_assocation_order=8, max_pwd_len=11)
    markov_obj_meh.set_values(training_data, char_markov_model, association_markov_model, association_rules, association_rule_path)

    '''
    markov_obj_meh = Markov_Attempt.Runner.Create_Password_Guesses(initilize_here=True,
                                                               training_data_path="/Users/thomasbekman/Documents/Research/Passwords/Cracked_Passwords/Use_me.txt",
                                                               association_rule_path="/Users/thomasbekman/Documents/Research/SpadeFiles/MinSup20000,MinConf0.1_HalfData/Patterns_halfData.txt",
                                                               char_markov_order=4, char_assocation_order=8,
                                                               max_pwd_len=11)
    '''
    try:
        print("state 3")

        for get_next_password in markov_obj_meh:
            #iteration_num +=1
            #rint(iteration_num)
            #print("state4")
            #print("Yes_Man")
            #print(multiprocessing.current_process())

            #print(get_next_password)

            if (get_next_password != None):
                count += 1
            if(get_next_password != None and get_next_password == password):
                print("password")
                print(password)
                print("password_guess")
                print(get_next_password)
                print(count,password)
                return (count,password)
        print("state 4")
        print("-------")
    except:
        print("failure")
        pass


# function to be mapped over
def calculateParallel(passwords, threads=12):   #Thread number should really be: threads=multiprocessing.cpu_count()
    '''
    # 33.27 #Parallel to Use
    pool = ThreadPool(threads)
    results = pool.map_async(find_number_guesses, passwords)
    pool.close()
    pool.join()
    return results
    '''



    '''
    #Non-Parallel
    to_return = []
    for i in passwords:
        find_number_guesses(i)
        to_return.append(find_number_guesses(i))
    '''


    '''
    #Different parallel but works the smae
    jobs = []
    for i in ["54323", "asdasdas", "sdsadasdasd", "345", "edccg"]:
        p = multiprocessing.Process(target=find_number_guesses, args=(i))
        jobs.append(p)
        p.start()
        print("Process: " + str(i) + "made.")
    for proc in jobs:
        proc.join()
    '''


    with Pool(threads) as p:
        #results = p.map(find_number_guesses, passwords)
        p.map(find_number_guesses, passwords)
    #results = pool.map(find_number_guesses, passwords)
    # pool.close()
    # pool.join()
    pass
    #return results


def run_grading(test_dataset_path):
    #test_data is a set of passwords
    test_data = [] #This should be fine as long as the test dataset is under 10 billion on the lab server (that would be approx 190GB)
    with open(test_dataset_path) as f:
        for line in f:
            print("1")
            print(line)
            #find_number_guesses(line.strip())
            test_data.append(line.strip())
    '''
    for i in test_data:
        find_number_guesses(i)
    '''
    guesses = calculateParallel(test_data)
    '''
    print("blah")
    guesses = calculateParallel(test_data)
    print(guesses)
    #tom = find_number_guesses("r23e123er23")
    #print(tom)
    '''
    '''
    for n in guesses:
        #print("new_test")
        #print(n)
        blah = n
        pass
    '''

start = time. time()

#markov_obj_meh = Markov_Attempt.Runner.Create_Password_Guesses(initilize_here=True, char_markov_order=4, char_assocation_order=8, max_pwd_len=11)

tom = Markov_Attempt.Runner.Create_Password_Guesses(
"/Users/thomasbekman/Documents/Research/Passwords/Cracked_Passwords/1k.txt",
"/Users/thomasbekman/Documents/Research/SpadeFiles/MinSup20000,MinConf0.1_HalfData/Patterns_halfData.txt", 3, 8,
11, True)


#markov_obj_meh.set_values(training_data, char_markov_model, association_markov_model, association_rules, association_rule_path)
#run_grading("/Users/thomasbekman/Documents/Research/Passwords/test_passwords/grading_test.txt")9

print("Training time")
end = time.time()
print(end - start)
'''
start = time.time()
tom.getPasswords()
with open("assoc_char_recursion.txt", "w+") as file:
    file.write(str(tom.passwords))
#end = time.time()
print("recursion approach")

end = time.time()
print(end - start)
'''



'''
print("test")
start = time.time()
a = tom.get_passwords_no_recusion_non_distributed("\t")
with open("non_distributed.txt", "w+") as file:
    file.write(json.dumps(a))
#print(a)
#tom.getPasswords()
end = time.time()
print(end - start)
'''




start = time.time()

#a = tom.get_passwords_no_recursion("",2)
#with open("assoc+char_noTree.txt", "w+") as file:
#    file.write(str(a))
#process = psutil.Process(os.getpid())
#print(process.memory_info().rss)

#end = time.time()

tom.distributed_generate_passwords()
end = time.time()
print(end - start)








#Test run grading @!!!!!!@
'''
try:
    for get_next_password in tom:
        print(get_next_password)

except:
    print("failure")
    pass
'''
'''
to_write = []
count = 0

while True:
    try:

        if count >6000:
            break
        D = tom.get_next()
        #print(D)
        if ("\n" in D[0][1]):
            count += 1
            if count % 200 == 0:
                print(str((count / 6000) * 100) + "%")
            #print(D)
            to_write.append(D[0][1])
        #file.write(D[0][1])
        if len(D[0][1]) >14:
            to_write.append(D[0][1])
            break



    except:
        print("Except")
        pass


print(to_write)
with open("char_overnight.txt", "w+") as file:
    file.write(str(to_write))



end = time.time()
print(end - start)
'''
#We

'''
def preprocess_passwords(association_pass_list,char_pass_list):
    to_check_dict = {}
    char_pass_to_use = []
    for password in char_pass_list:
        #As we now the char markov will 
        if("\n" not in password):
            char_pass_to_use

    for i in range(1,12):
        to_check_dict[i] = [[],[]]

    for i in association_pass_list:
        to_check_dict.get(len(i))[1].append(i)
    for i in char_pass_list:
        to_check_dict.get(len(i))[1].append(i)


'''

'''

def find_Unique(assocation_pass_list, char_pass_list):
    association_set = set(assocation_pass_list)
    char_set = set(char_pass_list)


    print("number of guesses from character markov")
    print(str(len(char_pass_list))+"\n")


    print("char_list_unique items")
    print(str(len(char_set))+"\n")

    print("number of guesses from association markov")
    print(str(len(assocation_pass_list))+"\n")

    print("assocation list unique items")
    print(str(len(association_set))+"\n")

    print("Percent of association is unique")
    print(str(len(association_set.difference(char_set))/len(association_set))+"\n")


    print("Intersection")
    print(str(len(association_set.intersection(char_set)))+"\n")

    print("In association, but not char")
    print(str(len(association_set.difference(char_set)))+"\n")
'''










#a = tom.assocation_pass
#b = tom.char_pass

#find_Unique(a,b)


a ="m,eh"
end = time.time()
print(end - start)



