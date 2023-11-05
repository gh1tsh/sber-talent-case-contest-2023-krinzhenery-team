from src.countVectorizer import *

# Расстояние L1
def distance_L1(left:str, right:str)->float:
    vec = countVectorize(left,right)
    distance = 0
    for i in range(len(vec[0])):
        distance += abs(vec[0][i] - vec[1][i])
    return 1 - distance / (sum(vec[0]) + sum(vec[1]))

def is_rewrite_distance_L1(left:str, right:str, threshold:float)->bool:
    return distance_L1(left,right) > threshold
