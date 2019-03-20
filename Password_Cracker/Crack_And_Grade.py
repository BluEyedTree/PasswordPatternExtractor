
from multiprocessing.pool import ThreadPool
import multiprocessing
import Markov_Attempt.Runner

Runner =  Markov_Attempt.Runner
maximum_password_length = 14


def find_number_guesses(password):
    count = 0
    for get_next_password in Runner.get_next(12):
        count +=1
        if(get_next_password == password):
            return (count,password)

        else:
            return (0, password)




# function to be mapped over
def calculateParallel(numbers, threads=multiprocessing.cpu_count()):
    pool = ThreadPool(threads)
    results = pool.map(squareNumber, numbers)
    pool.close()
    pool.join()
    return results


if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5]
    squaredNumbers = calculateParallel(numbers, 4)
    for n in squaredNumbers:
        print(n)

'''
from multiprocessing.dummy import Pool as ThreadPool


def squareNumber(n):
    return n ** 2


# function to be mapped over
def calculateParallel(numbers, threads=2):
    pool = ThreadPool(threads)
    results = pool.map(squareNumber, numbers)
    pool.close()
    pool.join()
    return results


if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5]
    squaredNumbers = calculateParallel(numbers, 4)



'''

