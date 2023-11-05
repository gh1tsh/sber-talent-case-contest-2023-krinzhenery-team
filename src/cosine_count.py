import numpy as np
from numpy.linalg import norm
from countVectorizer import *

#Косинусное сходство при векторизации count
def cosine_count(left : str,right : str) -> float:
    vec = countVectorize(left,right)
    return np.dot(vec[0],vec[1])/(norm(vec[0])*norm(vec[1]))

def is_rewrite_cosine_count(left : str,right : str, threshold : float) -> bool:
    return cosine_count(left,right) > threshold