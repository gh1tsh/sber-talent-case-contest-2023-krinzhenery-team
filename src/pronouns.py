import pandas as pd

def build_pronoun_dictionary(line):
    words = line.split(" ")
    pronouns =  set(pd.read_json('./../data/pronouns.json')[0].tolist())
    result = {}
    for key in pronouns:
        result[key] = 0
    for word in words:
        if (word in pronouns):
            result[word] += 1
    return result

def check_pronoun_correspondence(line1 : str, line2 : str) -> bool:
    dict1 = build_pronoun_dictionary(line1)
    dict2 = build_pronoun_dictionary(line2)
    return dict1 == dict2