# Простой подсчет слов
def word_set(left : str, right : str) -> float: 
    left = set(left.split(' '))
    right = set(right.split(' '))
    return 1 - len((left - right) | (right - left)) / len(left | right)

def is_rewrite_word_set(left : str, right : str, threshold : float) -> bool: 
    return word_set(left,right) > threshold