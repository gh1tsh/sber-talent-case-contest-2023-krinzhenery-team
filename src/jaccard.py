# коэффициент Жаккарда
def Jaccard(left : str, right : str) -> float:
    a = set(left)
    b = set(right)
    c = (a & b)
    up = len(c)
    down = len(a) + len(b) - len(c)
    if(down != 0):
        return up/down
    else:
        return 1.0 

def is_rewrite_Jaccard(left : str, right : str, threshold : float) -> bool:
    return Jaccard(left,right) > threshold