
# Данная функция рассчитывает расстояние Дамерау-Левенштейна между двумя заданными строкам (left и right)
def damerau_levenshtein_distance(left: str, right: str) -> float:
    d = {}
    first_str_len = len(left)
    second_str_len = len(right)
    
    for i in range(-1,first_str_len + 1):
        d[(i, -1)] = i + 1
    for j in range(-1,second_str_len + 1):
        d[(-1, j)] = j + 1

    for i in range(first_str_len):
        for j in range(second_str_len):
            if left[i] == right[j]:
                cost = 0
            else:
                cost = 1
            d[(i,j)] = min(
                           d[(i - 1, j)] + 1,      # удаление
                           d[(i, j - 1)] + 1,      # вставка
                           d[(i - 1, j - 1)] + cost  # замена
                          )
            if i and j and left[i] == right[j - 1] and left[i - 1] == right[j]:
                d[(i,j)] = min (d[(i, j)], d[i - 2, j - 2] + cost) # транспозиция

    return 1 - (d[first_str_len - 1, second_str_len - 1] / max(len(left), len(right))) # простая метрика

def is_rewrite_damerau_levenshtein_distance(left: str, right: str, threshold: float) -> bool:
    return damerau_levenshtein_distance(left, right) > threshold
