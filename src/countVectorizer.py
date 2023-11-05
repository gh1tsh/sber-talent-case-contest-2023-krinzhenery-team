from sklearn.feature_extraction.text import CountVectorizer

def countVectorize(left,right):
    countVectorizer = CountVectorizer()
    countVector = countVectorizer.fit_transform([left,right])
    return countVector.toarray()