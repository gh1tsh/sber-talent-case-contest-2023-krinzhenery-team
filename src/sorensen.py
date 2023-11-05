# Коэффииент Серенсена
def Sorensen(left : str, right : str) -> float:
    a = set()
    b = set()
    for i in range(len(left)-1):
        a.add(left[i] + left[i+1])
    for i in range(len(right)-1):
        b.add(right[i] + right[i+1])
    return 2 * len(a & b) / (len(a) + len(b))

def is_rewrite_Sorensen(left : str, right : str, threshold : float) -> bool:
    return Sorensen(left,right) > threshold