from pymongo import MongoClient

def read_association_rules_into_memory(path__to_association_rules):
    association_rules = {}
    with open(path__to_association_rules) as f:
        lines = f.readlines()
    for line in lines:
        score = float(line.split(",")[1])
        first_word = line.split("->")[0]
        second_word = line.split("->")[1].split(",")[0]

        if(first_word  in association_rules):
            association_rules[first_word][second_word] = score

        else:
            association_rules[first_word] = {second_word:score}


    return association_rules


def read_common_substrings_into_memory(cutoff):
    client = MongoClient('localhost', 27017)
    db = client['Substring_Research']  # Might have to change this back to mydb
    collection = db["substring_Length3to8"]
    #Based on running extract_top_x_Percentage substring it was found that the top %1 of common substrings happen over 176
    #start_time = time.time()
    substrings_cursor =  collection.find({"value":{"$gt": cutoff}})#Returns all items where the value is greater than 76
    list_to_return = list(substrings_cursor)
    #print("Mongo", time.time() - start_time, "s to run")

    return list_to_return