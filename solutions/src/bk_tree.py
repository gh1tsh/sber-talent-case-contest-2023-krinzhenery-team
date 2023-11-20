import json
import pandas as pd
import numpy as np
from collections import deque
from tqdm.auto import tqdm
from ipywidgets import FloatProgress


# Расстояние Левенштейна для расчета расстояния между вершинами дерева
def levenshtein(data1, data2):
    size_x = len(data1) + 1
    size_y = len(data2) + 1
    matrix = np.zeros((size_x, size_y))
    for x in range(size_x):
        matrix[x, 0] = x
    for y in range(size_y):
        matrix[0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if data1[x - 1] == data2[y - 1]:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1],
                    matrix[x, y - 1] + 1
                )
            else:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1] + 1,
                    matrix[x, y - 1] + 1
                )
    return (matrix[size_x - 1, size_y - 1])


# Класс-вершина дерева
class node:
    def __init__(self, word_id):
        self.word_id = word_id
        self.edges = dict()

# BK-дерево для поиска корректных слов
class bk_tree:
    def __init__(self, words, rates):
        self.words = words
        self.rates = rates
        self.root = None
        self.size = 0
    
    # Построение дерево по словарю
    def build(self):        
        for i in tqdm(range(len(self.words))):
            self.add_word(i)
    
    # Сохранение структуры дерева в файл
    def save(self, filepath):
        routes = []
        order = deque()
        order.append(self.root)
        visited = [False] * len(self.words)
        while (len(order) != 0):
            current_node = order.popleft()
            if (not visited[current_node.word_id]):
                visited[current_node.word_id] = True
                for key, value in current_node.edges.items():
                    order.append(value)
                    routes.append([current_node.word_id, value.word_id, key])
        
        with open(filepath, 'w', encoding='utf-8') as outfile:
            json.dump(routes, outfile, ensure_ascii=False)
    
    # Загрузка структуры дерева из файла
    def load(self, filepath):
        routes = pd.read_json(filepath).values.tolist()
        vertexes = [node(i) for i in range(len(self.words))]
        self.root = vertexes[0]
        for i in tqdm(range(len(routes))):
            edge = routes[i]
            source = edge[0]
            destination = edge[1]
            distance = edge[2]
            vertexes[source].edges[distance] = vertexes[destination]
        self.size = len(self.words)
        self.rate = [1] * len(self.words)
    
    # Добавление слова в дерево
    def add_word(self, word_id):
        if (self.root == None):
            self.root = node(word_id)
            self.size += 1
            return
        current_node = self.root
        while (current_node != None):
            current_word = self.words[current_node.word_id]
            insert_word = self.words[word_id]
            distance = levenshtein(current_word, insert_word)
            if (distance == 0):
                return
            if (distance not in current_node.edges):
                current_node.edges[distance] = node(word_id)
                self.size += 1
                return
            else:
                current_node = current_node.edges[distance]
    
    # Поиск ближайшего корректного слова
    def find_correct(self, pattern, error_limit):
        result = []
        order = deque()
        order.append(self.root)
        while (len(order) != 0):
            current_node = order.popleft()
            current_word = self.words[current_node.word_id]
            distance = levenshtein(pattern, current_word)
            if (distance <= error_limit):
                result.append((distance, abs(len(pattern) - len(current_word)), -self.rates[current_node.word_id], current_word))
            left = min(1, distance - error_limit)
            right = distance + error_limit
            for key, value in current_node.edges.items():
                if (key >= left and key <= right):
                    order.append(value)
        result.sort()
        if (len(result) == 0):
            return pattern
        else:
            return result[0][3]
           