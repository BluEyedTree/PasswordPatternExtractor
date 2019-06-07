import random

def random_sampler(filename, k):
	sample = []
	with open(filename) as f:
		for n, line in enumerate(f):
			if n < k:
				sample.append(line.rstrip())
			else:
				r = random.randint(0, n)
				if r < k:
					sample[r] = line.rstrip()
	return sample


def create_train_test_data(test_number, train_number, source_file):

	with open("test_data.txt", "w") as file_to_write:
		test_data = random_sampler(source_file, test_number)
		for line in test_data:
			file_to_write.write(line +"\n")


	with open("train_data.txt", "w") as file_to_write:
		train_data = random_sampler(source_file, train_number)
		for line in train_data:
			file_to_write.write(line +"\n")


create_train_test_data(1000000, 10000000,"/home/thomas/git/PasswordPatternExtractor/Data/UTF8_Formatted.txt")