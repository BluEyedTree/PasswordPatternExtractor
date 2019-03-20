from multiprocessing.pool import ThreadPool
import multiprocessing
import Markov_Attempt.Runner
import Markov_Attempt.Runner

Markov_Attempt.Runner
Runner =  Markov_Attempt.Runner
maximum_password_length = 14



'''
print("test")
for i in Runner.generatePasswords():
    print(i)
print("test")
'''



def find_number_guesses(password):
    count = 0
    print("state 2")
    try:
        for get_next_password in Markov_Attempt.Runner.Create_Password_Guesses("/Users/thomasbekman/Documents/Research/Passwords/Cracked_Passwords/1.txt", "/Users/thomasbekman/Documents/Research/SpadeFiles/MinSup20000,MinConf0.1_HalfData/Patterns_halfData.txt", 4, 8, 11):
            #print("Yes_Man")

            if (get_next_password != None):
                count += 1
            if(get_next_password != None and get_next_password == password):
                print("password")
                print(password)
                print("password_guess")
                print(get_next_password)
                return (count,password)

    except:
        print("failure")
        pass


# function to be mapped over
def calculateParallel(passwords, threads=multiprocessing.cpu_count()):
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

    guesses = calculateParallel(test_data)
    print(guesses)
    '''
    for n in guesses:
        #print("new_test")
        #print(n)
        blah = n
        pass
    '''


run_grading("/Users/thomasbekman/Documents/Research/Passwords/test_passwords/grading_test.txt")