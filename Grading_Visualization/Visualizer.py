import glob
import matplotlib.pyplot as plt

#For cracking visualization
#Number of guesses on X
#Number of cracked Y
def plot_crack_calculation(char_filepath,char_assoc_filepath):
    #path = "/Users/thomasbekman/graded_password_char_Maybe"


    filepath_1 = char_filepath
    filepath_2 = char_assoc_filepath

    count_of_passwords = 0
    guess_count = 0
    num_cracked_list =[0]
    num_guesses_list =[0]

    all_files = glob.glob(filepath_1)
    for file in all_files:
        with open(file, "r") as file_to_read:
            for line in file_to_read:
                try:

                    count_of_passwords += 1

                    stuff = line.split(",")
                    if(stuff[0] != "0"):
                        guess_count += int(stuff[0])
                        num_guesses_list.append(guess_count)
                        num_cracked_list.append(count_of_passwords)
                except:
                    pass


    count_of_passwords = 0
    guess_count = 0
    num_cracked_list_1 =[0]
    num_guesses_list_1 =[0]

    all_files = glob.glob(filepath_2)
    for file in all_files:
        with open(file, "r") as file_to_read:
            for line in file_to_read:
                try:

                    count_of_passwords += 1

                    stuff = line.split(",")
                    if(stuff[0] != "0"):
                        guess_count += int(stuff[0])
                        num_guesses_list_1.append(guess_count)
                        num_cracked_list_1.append(count_of_passwords)
                except:
                    pass



    #plt.axis([1, 10000, 1, 100000])
    plt.loglog()
    char_line, = plt.plot(num_cracked_list, num_guesses_list)
    assoc_line, = plt.plot(num_cracked_list_1, num_guesses_list_1)


#    plt.legend(handles=[char_line, assoc_line])
    plt.legend((char_line, assoc_line), ('Char Alone', 'Char + Association'))



    plt.xlabel("Number of Passwords Cracked")
    plt.ylabel("Number of Guesses")
    plt.show()
plot_crack_calculation("/Users/thomasbekman/graded_password_char_Maybe/*","/Users/thomasbekman/graded_password_assoc/*")
#Further Analysis

'''
Analyzes the number of passwords that are cracked.
pass_count: Total number of passwords in that file. This is 99% Accurate as there are some lines with multiple passwords. This is a bug.
total_count: Total number of passwords that are cracked. 
f_count: Total number of line with more than one password. This is a bug.  
'''

def password_crack_count(path):
    #path = "/Users/thomasbekman/graded_password_char_Maybe"

    pass_count =0
    total_count = 0
    f_count =0
    all_files = glob.glob(path)
    for file in all_files:
        with open(file, "r") as file_to_read:
            for line in file_to_read:
                pass_count += 1
                try:
                    stuff = line.split(",")
                    if(stuff[0] != "0"):
                        total_count +=1
                except:
                    f_count +=1
                    pass
    return total_count, f_count, pass_count
print(password_crack_count("/Users/thomasbekman/graded_password_char_Maybe/*"))


#Average Number of guesses until a password is cracked.
def average_guesses_to_crack(path):
    #path = "/Users/thomasbekman/graded_password_char_Maybe"

    count_of_passwords = 0
    guess_count = 0

    all_files = glob.glob(path)
    for file in all_files:
        with open(file, "r") as file_to_read:
            for line in file_to_read:
                try:
                    count_of_passwords += 1
                    stuff = line.split(",")
                    if(stuff[0] != "0"):
                        guess_count += int(stuff[0])
                except:
                    pass
    return guess_count/count_of_passwords
#print(average_guesses_to_crack("/Users/thomasbekman/graded_password_char_Maybe/*"))



def compare_runs(char_filepath, char_assoc_filepath):
    print("Char Number of Total Passwords cracked: " + str(password_crack_count(char_filepath)[0]))
    print("Char + Assocation Passwords Cracked: " + str(password_crack_count(char_assoc_filepath)[0]))

    print("")

    print("Char Number of Average Guesses to Crack a  Password: " + str(average_guesses_to_crack(char_filepath)))
    print("Char + Association Number of Average Guesses to Crack a Password: " + str(average_guesses_to_crack(char_assoc_filepath)))


    print("")

    plot_crack_calculation(char_filepath, char_assoc_filepath)


compare_runs("/Users/thomasbekman/graded_password_char_Maybe/*","/Users/thomasbekman/graded_password_assoc/*")








