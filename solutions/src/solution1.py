from src import load_dataset
from src import karlovskiy_distance
from src import word_set
from src import hamming_distance_custom
from src import cosine_tfidf
from src import jaro_winkler
from src import pronouns
import pandas as pd
from tqdm.auto import tqdm
from ipywidgets import FloatProgress

# Решение 1. Фильтрация

# Функция фильтрации на основе алгоритма верификации рерайтов (function) и заданного ограничения (threshold) 
# c возможностью проверки наборов местоимений (check_pronoun) 
def filter(df, groups,function,threshold,check_pronoun=True):
    for i in tqdm(range(len(df))):
        if df['used'][i]:  # Проверка метки использования строки
            continue
        groups.append([])
        groups[-1].append(df['text'][i])
        df['used'][i] = True
        
        for j in range(i+1,len(df)):
            if df['used'][j]: # Проверка метки использования строки
                continue
            if check_pronoun:
                if(function(df['text_preprocess'][i],df['text_preprocess'][j],threshold) and pronouns.check_pronoun_correspondence(df['text_preprocess'][i],df['text_preprocess'][j])):
                    groups[-1].append(df['text'][j])
                    df['used'][j] = True
            else:
                if(function(df['text_preprocess'][i],df['text_preprocess'][j],threshold)):
                    groups[-1].append(df['text'][j])
                    df['used'][j] = True
        if len(groups[-1]) == 1: # Если строка не имеет рерайта, то группа не формируется
            df['used'][i] = False 
            groups = groups[:-1]
    return groups

def group_by_filtering(filepath):
    df = pd.read_json(filepath)
    df['text_preprocess'] = df['text'].apply(load_dataset.preprocess_text)
    pd.options.mode.chained_assignment = None # Убираем лишние предупреждения
    df['used'] = [False] * len(df)
    groups = []
    # Фильтрация на основе алгоритмов верификации рерайтов
    groups = filter(df, groups,karlovskiy_distance.is_rewrite_karlovskiy_distance,0.89,check_pronoun=True)
    groups = filter(df, groups,word_set.is_rewrite_word_set,threshold=0.99,check_pronoun=False)
    groups = filter(df, groups,hamming_distance_custom.is_rewrite_hamming_distance_custom,threshold=0.9,check_pronoun=False)
    groups = filter(df, groups,cosine_tfidf.is_rewrite_cosine_tfidf,0.7,check_pronoun=True)
    groups = filter(df, groups,jaro_winkler.is_rewrite_jaro_winkler,0.9,check_pronoun=True)
    # Добавляем уникальные строки (не имеющие рерайт)
    groups = groups + [[str] for str in list(df[df['used']==False]['text'])]
    df = df.drop('used',axis=1)
    return groups

    