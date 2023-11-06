from src import load_dataset
from src import cosine_count
from src import dam_lev_dist
from src import distance_L2
from src import ngrams
from src import pronouns
from src import hamming_distance_custom


# Функция группировки строк
def find_groups(data):
    groups = []                        # Cписок для сохранения групп
    threshold = 0.9                    # Ограничение для алгоритмов верификации рерайтов
    used = [False for _ in range(len(data))]    # Список меток использования строк
    for current_id in range(len(data)):
        if (used[current_id]):
            continue
        current_group = []             # Текущая группа
        current_group.append(data[current_id])
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
                if (pronouns.check_pronoun_correspondence(line1, line2) or hamming_distance_custom.is_rewrite_hamming_distance_custom(line1, line2, 0.95)):
                    current_group.append(line2)  # Добавление строки в текущую группу
                    used[next_id] = True
        groups.append(current_group)             # Добавление сформированной группы к результирующему списку
    return groups

def group_by_equal_vote(filepath):
    data = load_dataset.load(filepath)
    groups = find_groups(data)
    return groups
    