import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from retriv import get_documents, get_query, get_ground_truth
import math
# hyperparamter for bm25
k_1 = 1.2 # single value
b = 0.8 # single value

def get_bm25_idf(query):
    doc_set, doc_id, doc_text = get_documents()
    documents = []
    for key, values in doc_set.items():
        documents.append(values)
    vectorizer = CountVectorizer(stop_words='english')
    documents_vectorized = vectorizer.fit_transform(documents)
    vocabulary = vectorizer.get_feature_names_out()
    dataframe = pd.DataFrame(documents_vectorized.toarray(), columns=vocabulary)



    # calculating ifds for the given documents
    dfs = (dataframe > 0).sum(axis=0)
    N = len(documents)
    idfs = np.log(N/dfs)

    dls = [len(docs) for docs in documents ] # vector
    avgdl = np.mean(dls) # single value
    numerator = np.array((k_1 + 1) * dataframe)
    denominator = np.array(k_1 *((1 - b) + b * (dls / avgdl))).reshape(N,1) + np.array(dataframe)


    BM25_tf = numerator/denominator
    idfs = np.array(idfs)
    BM25_score = idfs*BM25_tf


    bm25_idf = pd.DataFrame(BM25_score, columns=vocabulary)


    q_terms = query.split(" ")

    try:
        q_terms_only_df = bm25_idf[q_terms]
        score_q_d = q_terms_only_df.sum(axis=1)
        ranking = sorted(zip(documents,score_q_d.values), key = lambda tup:tup[1], reverse=True)
        # return ranking
        return sorted(zip(bm25_df.index.values,score_q_d.values), key = lambda tup:tup[1], reverse=True)
    except:
        return -1
    # for index, docs in enumerate(ranking):
    #     if index == 10:
    #         break
    #     print(docs)
# print(type(get_bm25_idf("zuckerman")))
def precision_at_k(k=20):
    doc_ranking = get_bm25_idf(query)
if __name__=='__main__':
    rel_set = get_ground_truth()
    qry_set, qry_id = get_query()
    for id, doc in rel_set.items():
        print("query = ", qry_set[str(id)], end="")
        doc_ranking = get_bm25_idf(qry_set[str(id)])
        if doc_ranking == -1:
            print("<-------------> no doc found")
        else:
            retrieved = [doc[0] for doc in doc_ranking[:20]]
            print(retrieved)
        # relevant_docs = 0
        # for index, (qry_id, doc_ids) in enumerate(rel_set.items()):
