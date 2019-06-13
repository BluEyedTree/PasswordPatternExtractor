import glob


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






for i in get_first_X_guesses("/Users/thomasbekman/git/PasswordPatternExtractor/Password_Cracker/final_formatted_password_store/*",100):
    print(i)

