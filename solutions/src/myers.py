# Алгоритм Майерса
def myers(left : str, right : str) -> float:
    m = len(left)
    n = len(right)
    
    # Инициализация матрицы
    matrix = [[0] * (n+1) for _ in range(m+1)]
    for i in range(m+1):
        matrix[i][0] = i
    for j in range(n+1):
        matrix[0][j] = j
    
    # Заполнение матрицы
    for i in range(1, m+1):
        for j in range(1, n+1):
            if left[i-1] == right[j-1]:
                matrix[i][j] = matrix[i-1][j-1]
            else:
                matrix[i][j] = min(matrix[i-1][j] + 1, # удаление
                                    matrix[i][j-1] + 1, # вставка
                                    matrix[i-1][j-1] + 1) # замена
    
    return 1 - matrix[m][n] / max(m,n)

def is_rewrite_myers(left : str, right : str, threshold : float) -> bool:
    return myers(left,right) > threshold