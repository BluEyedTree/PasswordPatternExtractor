import pickle
'''
Takes the score list that was pickled, and dumps it to a text file
'''
with open("scoress.txt", "w+") as infile:
    f = open('scores.pkl', 'rb')  # 'r' for reading; can be omitted
    value_list = pickle.load(f)  # load file content as mydict

    totalList = sorted(value_list, key=lambda x: x[0], reverse=True)
    #print(totalList)
    for item in totalList:
        infile.write(str(item)+"\n")