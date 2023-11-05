from math import floor

# Расстояние Джаро
def jaro_distance(left:str, right:str):
     
    if (left == right):
        return 1.0
 
    len1 = len(left)
    len2 = len(right)
    max_dist = floor(max(len1, len2) / 2) - 1
 
    match = 0
 
    hash_left = [0] * len(left)
    hash_right = [0] * len(right)
 
    for i in range(len1):
 
        for j in range(max(0, i - max_dist), 
                       min(len2, i + max_dist + 1)):
             
            if (left[i] == right[j] and hash_right[j] == 0):
                hash_left[i] = 1
                hash_right[j] = 1
                match += 1
                break
 
    if (match == 0):
        return 0.0
 
    t = 0
    point = 0
 
    for i in range(len1):
        if (hash_left[i]):
            while (hash_right[point] == 0):
                point += 1
 
            if (left[i] != right[point]):
                t += 1
            point += 1
    t = t//2
 
    return (match/ len1 + match / len2 + (match - t) / match)/ 3.0

# Расстояние Джаро-Винклера
def jaro_Winkler(left : str, right : str) -> float: 
 
    jaro_dist = jaro_distance(left, right); 
 
    if (jaro_dist > 0.7) :
 
        prefix = 0; 
 
        for i in range(min(len(left), len(right))) :
         
            if (left[i] == right[i]) :
                prefix += 1; 
 
            else :
                break; 
 
        prefix = min(4, prefix); 
        jaro_dist += 0.1 * prefix * (1 - jaro_dist); 
    return jaro_dist

def is_rewrite_jaro_winkler(left : str, right : str, threshold : float) -> bool:
    return jaro_Winkler(left,right) > threshold