from src import load_dataset
from src import cosine_count
from src import cosine_tfidf
from src import lev_dist
from src import dam_lev_dist
from src import distance_L1
from src import distance_L2
from src import hamming_distance_and_sequence_alignment_composition
from src import hamming_distance_custom
from src import hellinger
from src import jaccard
from src import jaro_winkler
from src import JSD
from src import karlovskiy_distance
from src import myers
from src import ngrams
from src import sorensen
from src import word_set
from src import pronouns
from src.Function import Function

import pandas as pd
from tqdm.auto import tqdm
from ipywidgets import FloatProgress


def group_by_ensemble(filepath):
    # Считывание и подготовка данных
    df = pd.read_json(filepath)
    df['text_preprocess'] = df['text'].apply(load_dataset.preprocess_text)
    strings = list(df['text_preprocess'])

    # Веса голосов для алгоритмов
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    EXTREME = 5

    # Пороговое значение (Если строки совпадают на значение больше, чем threshold, то строки считаются рерайтом)
    threshold = 0.85

    # Функции, участвующие в ансамбле
    functions = [Function(cosine_count.is_rewrite_cosine_count,threshold,MEDIUM),
                Function(cosine_tfidf.is_rewrite_cosine_tfidf,threshold,MEDIUM),
                Function(lev_dist.is_rewrite_levenshtein_distance,threshold,LOW),
                Function(dam_lev_dist.is_rewrite_damerau_levenshtein_distance,threshold,LOW),
                Function(distance_L1.is_rewrite_distance_L1,threshold,LOW),
                Function(distance_L2.is_rewrite_distance_L2,threshold,LOW),
                Function(hamming_distance_and_sequence_alignment_composition.is_rewrite_hamming_distance_normalized,threshold,LOW),
                Function(hamming_distance_custom.is_rewrite_hamming_distance_custom,threshold,LOW),
                Function(hellinger.is_rewrite_hellinger_distance,threshold,LOW),
                Function(jaccard.is_rewrite_Jaccard,threshold,MEDIUM),
                Function(jaro_winkler.is_rewrite_jaro_winkler,threshold,MEDIUM),
                Function(JSD.is_rewrite_JSD,threshold,MEDIUM),
                Function(karlovskiy_distance.is_rewrite_karlovskiy_distance,threshold,HIGH),
                Function(myers.is_rewrite_myers,threshold,LOW),
                Function(ngrams.is_rewrite_ngram,threshold,HIGH),
                Function(ngrams.is_rewrite_tverskiy_ngram,threshold,HIGH),
                Function(sorensen.is_rewrite_Sorensen,threshold,MEDIUM),
                Function(word_set.is_rewrite_word_set,threshold,MEDIUM),
                Function(pronouns.check_pronoun_correspondence,0,EXTREME)]

    # Убираем лишние предупреждения
    pd.options.mode.chained_assignment = None 

    df['used'] = [False] * len(df)
    groups = []

    # Цикл деления строк на группы
    for i in tqdm(range(len(df))):
        if df['used'][i]:  # Проверка метки использования строки
            continue
            
        groups.append([])
        groups[-1].append(df['text'][i])
        df['used'][i] = True
        
        for j in range(i+1,len(df)):
            if df['used'][j]: # Проверка метки использования строки
                continue
            
            # Подсчет голосов
            votes = sum([func.vote(df['text_preprocess'][i],df['text_preprocess'][j]) for func in functions])
            
            if(votes > 0):
                groups[-1].append(df['text'][j])
                df['used'][j] = True

        # Если строка не имеет рерайта, то группа не формируется
        if len(groups[-1]) == 1: 
            df['used'][i] = False 
            groups = groups[:-1]


    # Добавляем уникальные строки (не имеющие рерайт)
    groups = groups + [[str] for str in list(df[df['used']==False]['text'])]

    df = df.drop('used',axis=1)

    # Проверка, что строки не были взяты дважды
    assert(sum([len(group) for group in groups]) == len(df)) 

    return groups