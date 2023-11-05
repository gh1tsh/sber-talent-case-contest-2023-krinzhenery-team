import numpy as np
from numpy.linalg import norm
from src.tfidfVectorizer import *

#Косинусное сходство при векторизации tf-idf
def cosine_tfidf(left : str,right : str) -> float:
    vec = tfidfVectorize(left,right)
    return np.dot(vec[0],vec[1])/(norm(vec[0])*norm(vec[1]))

def is_rewrite_cosine_tfidf(left : str, right : str, threshold : float) -> bool:
    return cosine_tfidf(left,right) > threshold