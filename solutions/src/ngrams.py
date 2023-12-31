
# Общие функции

## Подсчет общего количества записей
def count_dictionary_entries(data):
    sum = 0
    for key, value in data.items():
        sum += value
    return sum


## Подсчет пересечения словарей
def count_dictionary_overlap(dict1, dict2):
    overlaps = 0
    for key, value1 in dict1.items():
        value2 = dict2.get(key, 0)
        overlaps += min(value1, value2)
    return overlaps


## Подсчет разницы между словарями
def count_dictionary_difference(dict1, dict2):
    result = 0
    for key, value1 in dict1.items():
        value2 = dict2.get(key, 0)
        result += max(0, value1 - value2)
    return result

# ngrams

## Построение словаря n-граммов размера batch_size для строки line
def build_ngrams(line, batch_size):
    result = {}
    if (len(line) < batch_size) :
        result[line] = 1
    else:
        for i in range(len(line) - batch_size):
            key = line[i: i + batch_size]
            if (' ' in key):
                continue
            old = result.get(key, 0)
            result[key] = old + 1
    return result


## Рассчет метрики похожести двух строк на основании n-граммов
def ngram_comparison(line1 : str, line2: str) -> float:
    dict1 = build_ngrams(line1, 2)
    dict2 = build_ngrams(line2, 2)
    cnt1 = count_dictionary_entries(dict1)
    cnt2 = count_dictionary_entries(dict2)
    overlaps = 0
    for key, value1 in dict1.items():
        value2 = dict2.get(key, 0)
        overlaps += min(value1, value2)
    return overlaps * 2 / (cnt1 + cnt2)

## Проверка двух строк на похожесть на основании ограничения threshold
def is_rewrite_ngram(line1 : str, line2 : str, threshold : float) -> bool:
    return ngram_comparison(line1, line2) > threshold


# Тверской индекс

## ## Рассчет Индекса Тверского похожести двух строк на основании n-граммов
def tverskiy_ngram_comparison(line1: str, line2: str) -> float:
    dict1 = build_ngrams(line1, 2)
    dict2 = build_ngrams(line2, 2)
    cnt_overlap = count_dictionary_overlap(dict1, dict2)
    cnt_difference1 = count_dictionary_difference(dict1, dict2)
    cnt_difference2 = count_dictionary_difference(dict2, dict1)
    return cnt_overlap / (cnt_overlap + 0.5 * cnt_difference1 + 0.5 * cnt_difference2)

## Проверка двух строк на похожесть на основании ограничения threshold
def is_rewrite_tverskiy_ngram(line1 : str, line2 : str, threshold : float) -> bool:
    return tverskiy_ngram_comparison(line1, line2) > threshold