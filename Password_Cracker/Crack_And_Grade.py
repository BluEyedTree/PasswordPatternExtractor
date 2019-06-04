import os
#import psutil
from multiprocessing.pool import Pool
import multiprocessing
import Markov_Attempt.Runner
import Markov_Attempt.Runner
import time
import json
from multiprocessing import Pool
import hashlib
import os
import copy
Markov_Attempt.Runner
import glob
Runner =  Markov_Attempt.Runner
maximum_password_length = 14




def get_pass_hash(password):
    arr = bytes(password, 'utf-8')
    hash = hashlib.md5(arr).digest()
    num = int.from_bytes(hash, "little")
    string_num = str(num)
    return string_num


def extract_password_and_count(line):
    removed_brackets = line[1:-2]
    number, non_formatted_password = removed_brackets.split(",")

    removed_quotation_marks_password = non_formatted_password[2:-1]
    return number, removed_quotation_marks_password

def find_number_guesses(password, order_number_files=2):
    pass_hash = get_pass_hash(password)
    file_name_final = pass_hash[-order_number_files:] + ".txt"
    count_found = None
    password_from_file_found = None

    #print("final_formatted_password_store/" + file_name_final)
    #Example file: [312, 'oveu']


    with open("final_formatted_password_store/" + file_name_final, "r") as file:
        for line in file:
            count, password_from_file = extract_password_and_count(line)
            if (password == password_from_file):
                count_found = count
                password_from_file_found = password_from_file



    with open("graded_password/"+file_name_final, "a") as file:
        if password_from_file_found is not None and count_found is not None:
            file.write(str(count_found) + "," + password_from_file_found + "\n")
        else:
            file.write(str(0) + "," + password + "\n")



# function to be mapped over
def calculateParallel(test_file="test_file.txt", threads=multiprocessing.cpu_count()):   #Thread number should really be: threads=multiprocessing.cpu_count()
    passwords = []
    with open(test_file, "r") as file:
        for line in file:
            passwords.append(line[:-1])


    with Pool(threads) as p:
        p.map(find_number_guesses, passwords)













start = time. time()

#markov_obj_meh = Markov_Attempt.Runner.Create_Password_Guesses(initilize_here=True, char_markov_order=4, char_assocation_order=8, max_pwd_len=11)

tom = Markov_Attempt.Runner.Create_Password_Guesses(
"train_data.txt",
"/home/thomas/git/PasswordPatternExtractor/Data/Patterns_halfData.txt", 3, 8,
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

#a = tom.get_passwords_no_recursion("\t",2)

tom.distributed_generate_passwords()


start = time.time()
calculateParallel(test_file="test_data.txt")
end = time.time()
print("Time to Grade against test_data: ")
print(end - start)

print("")
end = time.time()
print("Total Time: ")
print(end - start)



