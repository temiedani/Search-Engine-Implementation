from retriv import get_documents, get_query, get_ground_truth
import logging
# from run_doc2vec_lee import main
import os
import gensim
import numpy as np
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import h5py
import operator
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
def createEmbedding():
    doc_set, doc_id, doc_text = get_documents()
    qry_set, qry_id = get_query()
    rel_set = get_ground_truth()
    model = Doc2Vec.load('doc2vec.model')
    hf = h5py.File('vectors.h5', 'w')
    for id, text in doc_set.items():
        token = gensim.utils.simple_preprocess(text)
        vector =  model.infer_vector(token)
        hf.create_dataset(id, data=vector)
    print("Embedding for each document is done")



def get_similar_doc(query):
    doc_set, doc_id, doc_text = get_documents()
    model = Doc2Vec.load('doc2vec.model')
    hf = h5py.File('vectors.h5', 'r')
    qry_vector = model.infer_vector(gensim.utils.simple_preprocess(query))
    cosin_similarty = dict()
    for id, vector in hf.items():
        doc_vec = np.array(vector)

        cosin = np.dot(doc_vec, qry_vector)/(np.linalg.norm(doc_vec)*np.linalg.norm(qry_vector))

        cosin_similarty[id] = cosin

    sorted_cosin_sim = dict(sorted(cosin_similarty.items(), key=operator.itemgetter(1),reverse=True))
    docs = []
    for key, value in sorted_cosin_sim.items():
        docs.append( (doc_set[str(key)]+str(value) ))
    return docs
    # print("Top 10 doc by our vsm:-")
    # for index, (id, sim) in enumerate(sorted_cosin_sim.items()):
    #     if index == 10:
    #         break
    #     print(id, sim)
    # print("ground truth for qryid =  1")
    # rel_set = get_ground_truth()
    # for qryid, docid in rel_set.items():
    #     if qryid == "1":
    #         print(docid)

# print("=========>", type(get_similar_doc("will smith")))
# createEmbedding()
