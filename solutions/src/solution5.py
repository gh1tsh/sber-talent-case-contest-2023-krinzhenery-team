from src import bk_tree
from src import load_dataset
from src import pronouns
from src import hamming_distance_custom
from src import negatives
from src import word_collation

from tqdm.auto import tqdm
from ipywidgets import FloatProgress
import pandas as pd
import json


def fix_spelling(data, correct_tree):
    for i in tqdm(range(len(data))):
        line = data[i]
        words = line.split()
        for j in range(len(words)):
            words[j] = correct_tree.find_correct(words[j], 2)
        data[i] = ' '.join(words)
    return data


def build_word_dictionary(line):
    words = line.split()
    result = dict()
    for word in words:
        if len(word) >= 4:
            old = result.get(word, 0)
            result[word] = old + 1
    return result

def count_dict_entries(data):
    return sum([value for key, value in data.items()])


def word_set_correspondence(line1, line2):
    dict1 = build_word_dictionary(line1)
    dict2 = build_word_dictionary(line2)
    total_count = count_dict_entries(dict1) + count_dict_entries(dict2)
    intersection_count = 0
    for key, value1 in dict1.items():
        value2 = dict2.get(key, 0)
        intersection_count += min(value1, value2) * 2
    return intersection_count / total_count

def is_rewrite_word_set_correspondence(line1, line2, threshold):
    return word_set_correspondence(line1, line2) >= threshold


def count_negatives(line):
    words = line.split()
    negations = ["не", "ни"]
    negation_counters = [0] * len(negations)
    for word in words:
        for i in range(len(negations)):
            if word.startswith(negations[i]):
                negation_counters[i] += 1
    return sum(negation_counters)

def check_negative_corresponense(line1, line2):
    return (count_negatives(line1) % 2) == (count_negatives(line2) % 2)


# Функция группировки строк
def find_groups(data, base_data):
    groups = []                        # Cписок для сохранения групп
    used = [False for _ in range(len(data))]    # Список меток использования строк
    for current_id in tqdm(range(len(data))):
        if (used[current_id]):
            continue
        current_group = []             # Текущая группа
        current_group.append(base_data[current_id])
        used[current_id] = True
        for next_id in range(current_id + 1, len(data)):
            #print("\tNext id:", next_id)
            if (used[next_id]):
                continue
            line1 = data[current_id]
            line2 = data[next_id]
            # Проверка строк с помощью алгоритмов верификации
            if (word_collation.is_rewrite_word_collation(line1, line2, 0.85) and
               negatives.check_negative_corresponense(line1, line2) and
                    (pronouns.check_pronoun_correspondence(line1, line2) 
                        or (hamming_distance_custom.clean_hamming_distance(line1, line2) == 1))):
                current_group.append(base_data[next_id])  # Добавление строки в текущую группу
                used[next_id] = True
        groups.append(current_group)             # Добавление сформированной группы к результирующему списку
    return groups


def group_by_frequency_analysis(filepath):
    base_data = load_dataset.load(filepath)
    data = [load_dataset.preprocess_text(text) for text in base_data] # Убираем знаки препинания и лишние пробелы
    # Находим уникальные слова в датасете
    # Находим уникальные слова в датасете и их частоту
    actual_word_set = dict()
    for line in data:
        words = line.split()
        for word in words:
            old = actual_word_set.get(word, 0)
            actual_word_set[word] = old + 1
    # Загружаем орфографический словарь
    vocabulary_source = "../data/russian-utf8.json"
    vocabulary = pd.read_json(vocabulary_source)[0].tolist()
    # Загружаем имена
    names_source = "../data/names.json"
    names = pd.read_json(names_source)[0].tolist()
    vocabulary = vocabulary + names
    # Удаляем слова, которые не задействованы в датасете
    vocabulary = [item for item in vocabulary if item in actual_word_set]
    encounter_rate = [actual_word_set[word] for word in vocabulary]
    # Строим BK-дерево
    verification_tree = bk_tree.bk_tree(vocabulary, encounter_rate)
    verification_tree.build()
    data = fix_spelling(data, verification_tree)
    groups = find_groups(data, base_data)
    return groups