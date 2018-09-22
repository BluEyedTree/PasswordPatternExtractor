with open("/Users/thomasbekman/Documents/Research/Passwords/Cracked_Passwords/10-million-combos.txt", encoding="latin-1") as f:
    with open('./output.txt', 'a') as f1:
        for line in f:
            line = line.rstrip()
            try:
                password = line.split("\t")[1]
                username = line.split("\t")[0]
                print(line.split("\t"))
                f1.write(password + "\n")
            except:
                pass
