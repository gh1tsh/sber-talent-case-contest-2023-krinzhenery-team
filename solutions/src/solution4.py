from src import load_dataset
from src import karlovskiy_distance
from src import KMeans
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tqdm.auto import tqdm
from ipywidgets import FloatProgress
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from typing import List

import warnings
warnings.filterwarnings("ignore")


def clusterization(strings:List[str])->List[List[str]]:
    n_clusters = 2
    # Если в списке меньше n_clusters, то их нельзя поделить на n_clusters, поэтому возвращаем исходный список 
    if len(set(strings)) <= n_clusters:
        return [strings]
        
    # Векторизация подсчетом
    Vectorizer = CountVectorizer()
    vector = Vectorizer.fit_transform(strings)
    strings_vectorized = vector.toarray()

    # Нормализация 
    strings_vectorized = StandardScaler().fit_transform(strings_vectorized)

    # Уменьшение размерности с помощью метода главных компонент
    strings_vectorized_nD = PCA(n_components=len(strings_vectorized)//2).fit_transform(strings_vectorized)

    # Кластеризация методом К-средних
    model = KMeans.KMeans(n_clusters=n_clusters).fit(strings_vectorized_nD)

    # Группировка строк по получившимся кластерам
    clusters = {}
    for i in range(len(model.labels_)):
        if model.labels_[i] not in clusters:
            clusters[model.labels_[i]] = []
        clusters[model.labels_[i]].append(strings[i])

    return list(clusters.values())




def group_by_clusterization(filepath):
    # Считывание и подготовка данных
    df = pd.read_json(filepath)
    df['text_preprocess'] = df['text'].apply(load_dataset.preprocess_text)
    strings = list(df['text_preprocess'])
    
    # Итеративная кластеризация
    coef = 8 # Экспериментально подобранный коэффициент
    clusters = clusterization(strings)
    for iter in tqdm(range(len(strings)//coef)):
        for i,cluster in enumerate(clusters):
            clusters[i] = clusterization(cluster)
        clusters = [item for cluster in clusters for item in cluster]
    
    # Формирование групп
    groups = []
    threshold = 0.89
    for cluster in tqdm(clusters):
        if len(cluster) == 1:
            groups.append(cluster)
        # Дополнительная проверка с помощью расстояния Карловского
        if len(cluster) == 2:
            if karlovskiy_distance.is_rewrite_karlovskiy_distance(cluster[0],cluster[1],threshold):
                groups.append(cluster)  
            else:
                groups.append([cluster[0]])
                groups.append([cluster[1]])
        if len(cluster) > 2:
            used = [False] * len(cluster)
            for i in range(len(cluster)):
                if used[i]:
                    continue
                for j in range(i+1,len(cluster)):
                    if used[j]:
                        continue
                    if karlovskiy_distance.is_rewrite_karlovskiy_distance(cluster[i],cluster[j],threshold):
                        used[i] = True
                        used[j] = True
                        groups.append([cluster[i],cluster[j]])
            for i in range(len(cluster)):
                if not used[i]:
                    groups.append([cluster[i]])

    # Преобразование в строки исходного датасета
    for i in range(len(groups)):
        for j in range(len(groups[i])):
            groups[i][j] = df[df['text_preprocess'] == groups[i][j]]['text'].to_numpy()[0]
            
    return groups
