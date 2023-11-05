import re
import pandas as pd

def preprocess_text(text):
    text = text.lower()                  # Приводим текст к нижнему регистру
    text = re.sub(r'[^\w-]', ' ', text)  # Удаляем знаки препинания
    text = re.sub(r'_', ' ', text)       # Удаляем нижнее подчеркиваниее на всякий случай
    text = re.sub(r'\s+', ' ', text)     # Удаляем лишние пробелы
    text = text.replace('ё','е')         # заменяем ё на е
    return text.strip()

def load():
    df = pd.read_json('../data/sample.json')
    df['text'] = df['text'].apply(preprocess_text)
    return df['text'].tolist()