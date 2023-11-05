from sklearn.feature_extraction.text import TfidfVectorizer

def tfidfVectorize(left,right):
    tfidfVectorizer = TfidfVectorizer()
    tfidfVector = tfidfVectorizer.fit_transform([left,right])
    return tfidfVector.toarray()