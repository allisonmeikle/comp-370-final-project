from collections import Counter
import math
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
def get_tf_idf_scores_manual(articles: list[str]):
    """
    articles: list of strings, each entry represent an article
    """
    N = len(articles)
    if N == 0:
        return [], {}, {}
    doc_word_counts = []
    doc_word_freq = Counter()

    for article in articles:
        words = article.split()
        freqs = Counter(words)
        doc_word_counts.append(freqs)

        for word in freqs.keys():
            doc_word_freq[word] += 1

    #vocab = {word: x for x, word in enumerate(doc_word_freq.keys())}
    idf = {}
    for word, freq in doc_word_freq.items():
        idf[word] = math.log(N / freq)

    tf_idf = {}
    for doc_ind, doc_counter in enumerate(doc_word_counts):
        doc_len = sum(doc_counter.values())
        for word, count in doc_counter.items():
            if word not in tf_idf:
                tf_idf[word] = 0
            tf_idf[word] += count/doc_len
    for word in tf_idf:
        tf_idf[word] = tf_idf[word] * idf[word]
    
    return tf_idf

def get_tf_idf_scores_scipy(docs):
    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english"
    )
    X = vectorizer.fit_transform(docs)
    terms = vectorizer.get_feature_names_out()
    
    # Aggregate across all documents
    scores = np.asarray(X.sum(axis=0)).ravel()
    
    # Map terms to their aggregated TF-IDF scores
    tfidf_scores = dict(zip(terms, scores))
    return tfidf_scores


if __name__ == "__main__":
    df = pd.read_csv("../data/articles/nytimes.csv")
    docs = df['description'].tolist()

    tf_idf = get_tf_idf_scores_manual(docs)
    top_manual = sorted(tf_idf.items(), key=lambda x: x[1], reverse=True)[:10]
    print("MANUAL top scores:", top_manual)

    tf_idf = get_tf_idf_scores_scipy(docs)
    top_scipy = sorted(tf_idf.items(), key=lambda x: x[1], reverse=True)[:10]
    print("SCIPY top scores:", top_scipy)
    