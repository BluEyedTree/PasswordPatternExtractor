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

	with open("For_Kuntal_30k.txt", "w") as file_to_write:
		test_data = random_sampler(source_file, test_number)
		for line in test_data:
			file_to_write.write(line +"\n")


	with open("For_Kuntal_50", "w") as file_to_write:
		train_data = random_sampler(source_file, train_number)
		for line in train_data:
			file_to_write.write(line +"\n")


create_train_test_data(30000,50,"/home/thomas/git/PasswordPatternExtractor/Data/UTF8_Formatted.txt")