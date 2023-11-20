# Построение словаря ключевых слов
def build_word_dictionary(line):
    words = line.split()
    result = dict()
    for word in words:
        if len(word) >= 4:
            old = result.get(word, 0)
            result[word] = old + 1
    return result

# Посчитать общее количество вхождений слов
def count_dict_entries(data):
    return sum([value for key, value in data.items()])

# Функция расчета похожести двух строк по ключевым словам
def word_collation(line1, line2):
    dict1 = build_word_dictionary(line1)
    dict2 = build_word_dictionary(line2)
    total_count = count_dict_entries(dict1) + count_dict_entries(dict2)
    intersection_count = 0
    for key, value1 in dict1.items():
        value2 = dict2.get(key, 0)
        intersection_count += min(value1, value2) * 2
    return intersection_count / total_count

# Функция верификации рерайта на основе соответствия ключевых слов
def is_rewrite_word_collation(line1, line2, threshold):
    return word_collation(line1, line2) > threshold