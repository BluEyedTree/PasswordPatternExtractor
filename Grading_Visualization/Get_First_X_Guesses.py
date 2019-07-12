qimport glob


def get_first_X_guesses(path, num_guesses):
    first_x_guesses = []
    all_files = glob.glob(path)
    for file in all_files:
        with open(file) as text_file:
            for line in text_file:
                list_from_disk = line.strip()
                list_from_disk = list_from_disk.replace("/", "")
                list_from_disk = list_from_disk.replace("'", "")
                list_from_disk = list_from_disk.replace("[", "")
                list_from_disk = list_from_disk.replace("]", "")
                list_from_disk = list_from_disk.split(",")
                list_from_disk = [int(list_from_disk[0]),list_from_disk[1]]

                if list_from_disk[0]< num_guesses:
                    first_x_guesses.append((list_from_disk[0],list_from_disk[1]))


    first_x_guesses.sort()
    return first_x_guesses


def calcualte_avg_length(input_tuple_list):
    total = 0
    for i in input_tuple_list:
        total += len(i[1])

    print(total/len(input_tuple_list))



'''
for i in get_first_X_guesses("/Users/thomasbekman/git/PasswordPatternExtractor/Password_Cracker/final_formatted_password_store/*",100):
    print(i)
'''

#/home/thomas/git/PasswordPatternExtractor/Password_Cracker/Most_recent_run_3_char_alone/final_formatted_password_store
#/home/thomas/git/PasswordPatternExtractor/Password_Cracker/Most_recent_run_Run_3_Char_Assoc_Store/final_formatted_password_store
print("Char Alone Length")
print(calcualte_avg_length( get_first_X_guesses("/home/thomas/git/PasswordPatternExtractor/Password_Cracker/Most_recent_run_3_char_alone/final_formatted_password_store/*",100000000)))


print("Char + Association Length")
print(calcualte_avg_length( get_first_X_guesses("/home/thomas/git/PasswordPatternExtractor/Password_Cracker/Most_recent_run_Run_3_Char_Assoc_Store/final_formatted_password_store/*",100000000)))
