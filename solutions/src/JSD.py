import scipy.stats
import numpy as np
from src.countVectorizer import *

# Дивергенция Дженсена-Шеннона
def JSD(left:str, right:str)->float:
    vec = countVectorize(left,right)
    p = np.array(vec[0])
    q = np.array(vec[1])
    m = (p + q) / 2
    divergence = (scipy.stats.entropy(p, m) + scipy.stats.entropy(q, m)) / 2
    distance = np.sqrt(divergence)
    return 1 - distance

def is_rewrite_JSD(left:str, right:str, threshold:float)->bool:
    return JSD(left,right) > threshold