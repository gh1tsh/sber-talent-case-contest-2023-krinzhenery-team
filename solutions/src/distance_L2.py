from math import sqrt
from src.countVectorizer import *

# Расстояние L2
def distance_L2(left:str, right:str)->float:
    vec = countVectorize(left,right)
    distance = 0
    for i in range(len(vec[0])):
        distance += (vec[0][i] - vec[1][i])**2
    return 1 - sqrt(distance) / (sum(vec[0]) + sum(vec[1]))

def is_rewrite_distance_L2(left:str, right:str, threshold:float)->bool:
    return distance_L2(left,right) > threshold