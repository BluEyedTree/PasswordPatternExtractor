
totalCount = 0
removedCount = 0


iter_count = 0
rockYouLength = 24342374




with open("/Users/thomasbekman/Documents/Research/Passwords/Cracked_Passwords/totalList.txt", encoding="latin-1") as f:
    with open('/Users/thomasbekman/Documents/Research/Passwords/Cracked_Passwords/UTF8_Formatted.txt', 'a') as f1:
        for line in f:
            totalCount += 1
            line = line.rstrip("\n")
            iter_count += 1
            if (iter_count % 1000 == 0):
                print(str(iter_count / rockYouLength * 100) + str("% Done"))

            line1 = line.encode("utf-8").decode("utf-8")
            f1.write(line1 + "\n")







