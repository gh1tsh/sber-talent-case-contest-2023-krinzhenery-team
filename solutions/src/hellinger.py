from src.countVectorizer import *
import numpy as np

# Расстояние Хеллингера
def hellinger_distance(left:str,right:str)->float:
    vec = countVectorize(left,right)
    s = 0
    for p_i, q_i in zip(vec[0], vec[1]):
        s = (np.sqrt(p_i) - np.sqrt(q_i)) ** 2
    return 1 - np.sqrt(s / 2)
    
def is_rewrite_hellinger_distance(left:str,right:str, threshold:float)->bool:
    return hellinger_distance(left,right) > threshold