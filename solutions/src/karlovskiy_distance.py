# расстояние Карловского
def karlovskiy_distance(left : str, right : str) -> float:
    left = '\b\b' + left + '\f\f'
    right = '\b\b' + right + '\f\f'
    dist = -4
    for i in range(len(left) - 2):
        if left[i:i+3] not in right:
            dist += 1
    for i in range(len(right) - 2):
        if right[i:i+3] not in left:
            dist += 1
    return 1 - max(0, dist) / (len(left) + len(right) - 8)
    
def is_rewrite_karlovskiy_distance(left : str, right : str,threshold : float) -> bool:
    return karlovskiy_distance(left, right) > threshold