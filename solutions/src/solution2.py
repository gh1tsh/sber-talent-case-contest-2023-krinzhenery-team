from src import load_dataset
from src import cosine_count
from src import dam_lev_dist
from src import distance_L2
from src import ngrams
from src import pronouns
from src import hamming_distance_custom

from tqdm.auto import tqdm
from ipywidgets import FloatProgress


# Функция группировки строк
def find_groups(data, base_data):
    groups = []                        # Cписок для сохранения групп
    threshold = 0.9                    # Ограничение для алгоритмов верификации рерайтов
    used = [False for _ in range(len(data))]    # Список меток использования строк
    for current_id in tqdm(range(len(data))):
        if (used[current_id]):
            continue
        current_group = []             # Текущая группа
        current_group.append(base_data[current_id])
        used[current_id] = True
        for next_id in range(current_id + 1, len(data)):
            if (used[next_id]):
                continue
            line1 = data[current_id]
            line2 = data[next_id]
            # Проверка строк с помощью алгоритмов верификации
            if (cosine_count.is_rewrite_cosine_count(line1, line2, threshold) or
               dam_lev_dist.is_rewrite_damerau_levenshtein_distance(line1, line2, threshold) or
               distance_L2.is_rewrite_distance_L2(line1, line2, threshold) or
               ngrams.is_rewrite_tverskiy_ngram(line1, line2, threshold)):
                if (pronouns.check_pronoun_correspondence(line1, line2) or(hamming_distance_custom.clean_hamming_distance(line1, line2) == 1)):
                    current_group.append(base_data[next_id])  # Добавление строки в текущую группу
                    used[next_id] = True
        groups.append(current_group)             # Добавление сформированной группы к результирующему списку
    return groups

def group_by_general_coverage(filepath):
    base_data = load_dataset.load(filepath)
    data = data = [load_dataset.preprocess_text(text) for text in base_data]
    groups = find_groups(data, base_data)
    return groups
    