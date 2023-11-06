from sklearn.feature_extraction.text import TfidfVectorizer

## Векторизация с помощью TF-IDF
def tfidfVectorize(left,right):
    tfidfVectorizer = TfidfVectorizer()
    tfidfVector = tfidfVectorizer.fit_transform([left,right])
    return tfidfVector.toarray()