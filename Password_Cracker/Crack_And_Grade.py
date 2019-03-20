from multiprocessing.pool import ThreadPool
import multiprocessing
import Markov_Attempt.Runner

Markov_Attempt.Runner
Runner =  Markov_Attempt.Runner
maximum_password_length = 14


def find_number_guesses(password):
    count = 0
    for get_next_password in Runner.get_next(12):
        count +=1
        print("meh")
        print(get_next_password)
        if(get_next_password == password):
            return (count,password)

        else:
            return (0, password)




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
            test_data.append(line.strip())

    guesses = calculateParallel(test_data)
    for n in guesses:
        print(n)


