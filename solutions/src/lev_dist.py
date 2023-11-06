# Рассчет расстояния Левенштейна
def levenshtein_distance(left, right) -> float:
    m = len(left)
    n = len(right)

    d = [[0] * (n + 1) for i in range(m + 1)]  

    for i in range(1, m + 1):
        d[i][0] = i

    for j in range(1, n + 1):
        d[0][j] = j
    
    for j in range(1, n + 1):
        for i in range(1, m + 1):
            if left[i - 1] == right[j - 1]:
                cost = 0
            else:
                cost = 1
            d[i][j] = min(d[i - 1][j] + 1,        # Удаление
                          d[i][j - 1] + 1,        # Вставка
                          d[i - 1][j - 1] + cost) # Замена  

    return 1 - (d[m][n] / max(len(left), len(right)))

def is_rewrite_levenshtein_distance(left: str, right: str, threshold: float) -> bool:
    return levenshtein_distance(left, right) > threshold
