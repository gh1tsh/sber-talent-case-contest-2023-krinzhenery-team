from sklearn.feature_extraction.text import CountVectorizer

## Векторизация с помощью подсчета слов
def countVectorize(left,right):
    countVectorizer = CountVectorizer()
    countVector = countVectorizer.fit_transform([left,right])
    return countVector.toarray()