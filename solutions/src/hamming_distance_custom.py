def is_rewrite_hamming_distance_custom(left:str,right:str,threshold=0.9)->bool:
    if len(left) != len(right):
        return False
    c = 0
    for i in range(len(left)):
        c += left[i]!=right[i]
    return 1 - c / len(left) > threshold
