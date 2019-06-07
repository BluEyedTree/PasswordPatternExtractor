import ast
import json

def calculate_avg_length(iterable):
    total = 0
    for i in iterable:
        total+=len(i)

    return total/len(iterable)

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



    print("Diff")
    #print(char_set.difference(association_set))
    print(str(len(char_set.difference(association_set)) / len(association_set)) + "\n")


    print("Intersection")
    print(str(len(association_set.intersection(char_set)))+"\n")

    print("In association, but not char")
    print(str(len(association_set.difference(char_set)))+"\n")

    print("Max Association Length")
    print(max(assocation_pass_list, key=len))

    print("Max char length")
    print(max(char_pass_list, key=len))


    print("char_avg_length")
    print(calculate_avg_length(char_set))

    print("asoc_avg_length")
    print(calculate_avg_length(association_set))


char_list = []
assoc_list = []

'''
with open("char_distributed.txt", "r") as f:
    char_list = ast.literal_eval(f.read())

assoc_list = []

with open("distributed.txt","r") as f:

    assoc_list = ast.literal_eval(f.read())

'''


for i in range(10,30):
    char_num = str(i)
    print(char_num)

    print("")
    print("")
    '''
    print(assoc_num)

    print("")
    print("")
    '''

    with open("/home/thomas/git/PasswordPatternExtractor/Password_Cracker/Store_1/final_formatted_password_store_bak_1/"+char_num+".txt", "r") as file:
        for line in file:
            count, password_from_file = json.loads(line)
            assoc_list.append(password_from_file)

    with open("/home/thomas/git/PasswordPatternExtractor/Password_Cracker/final_formatted_password_store/"+char_num+".txt", "r") as file:
        for line in file:
            count, password_from_file = json.loads(line)
            char_list.append(password_from_file)



    find_Unique(assoc_list,char_list)
    char_list = []
    assoc_list = []



    #in_list = list(file.read())
    #print(in_list)