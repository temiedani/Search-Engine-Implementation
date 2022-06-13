r"""
Doc2Vec Model
=============

Introduces Gensim's Doc2Vec model and demonstrates its use on the
`Lee Corpus <https://hekyll.services.adelaide.edu.au/dspace/bitstream/2440/28910/1/hdl_28910.pdf>`__.

"""

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


import os
import gensim
test_data_dir = os.path.join(gensim.__path__[0], 'test', 'test_data')
lee_train_file = os.path.join(test_data_dir, 'lee_background.cor')
lee_test_file = os.path.join(test_data_dir, 'lee.cor')
import smart_open
import tempfile
def read_corpus(fname, tokens_only=False):
    with smart_open.open(fname, encoding="iso-8859-1") as f:
        for i, line in enumerate(f):
            tokens = gensim.utils.simple_preprocess(line)
            if tokens_only:
                yield tokens
            else:
                # For training data, add tags
                yield gensim.models.doc2vec.TaggedDocument(tokens, [i])
def main():
    train_corpus = list(read_corpus(lee_train_file))
    test_corpus = list(read_corpus(lee_test_file, tokens_only=True))
    # print("train corpus = ", train_corpus[:2])
    # print("test = ", test_corpus[:2])
    model = gensim.models.doc2vec.Doc2Vec(vector_size=50, min_count=2, epochs=40)
    model.build_vocab(train_corpus)
    # print(f"Word 'penalty' appeared {model.wv.get_vecattr('penalty', 'count')} times in the training corpus.")
    model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)
    # vector = model.infer_vector(['only', 'you', 'can', 'prevent', 'forest', 'fires'])
    # print(vector)
    model.save("doc2vec.model")
    # with tempfile.NamedTemporaryFile(prefix='gensim-model-', delete=False) as tmp:
    #     temporary_filepath = tmp.name
    #     model.save(temporary_filepath)
    # return model
main()



# similar documents.
#
# ranks = []
# second_ranks = []
# for doc_id in range(len(train_corpus)):
#     inferred_vector = model.infer_vector(train_corpus[doc_id].words)
#     sims = model.dv.most_similar([inferred_vector], topn=len(model.dv))
#     rank = [docid for docid, sim in sims].index(doc_id)
#     ranks.append(rank)
#
#     second_ranks.append(sims[1])

###############################################################################
# Let's count how each document ranks with respect to the training corpus
#
# NB. Results vary between runs due to random seeding and very small corpus
# import collections

# counter = collections.Counter(ranks)
# print(counter)

###############################################################################
# Basically, greater than 95% of the inferred documents are found to be most
# similar to itself and about 5% of the time it is mistakenly most similar to
# another document. Checking the inferred-vector against a
# training-vector is a sort of 'sanity check' as to whether the model is
# behaving in a usefully consistent manner, though not a real 'accuracy' value.
#
# This is great and not entirely surprising. We can take a look at an example:
#
# print('Document ({}): «{}»\n'.format(doc_id, ' '.join(train_corpus[doc_id].words)))
# print(u'SIMILAR/DISSIMILAR DOCS PER MODEL %s:\n' % model)
# for label, index in [('MOST', 0), ('SECOND-MOST', 1), ('MEDIAN', len(sims)//2), ('LEAST', len(sims) - 1)]:
#     print(u'%s %s: «%s»\n' % (label, sims[index], ' '.join(train_corpus[sims[index][0]].words)))

###############################################################################
# Notice above that the most similar document (usually the same text) is has a
# similarity score approaching 1.0. However, the similarity score for the
# second-ranked documents should be significantly lower (assuming the documents
# are in fact different) and the reasoning becomes obvious when we examine the
# text itself.
#
# We can run the next cell repeatedly to see a sampling other target-document
# comparisons.
#

# Pick a random document from the corpus and infer a vector from the model
# import random
# doc_id = random.randint(0, len(train_corpus) - 1)
#
# # Compare and print the second-most-similar document
# print('Train Document ({}): «{}»\n'.format(doc_id, ' '.join(train_corpus[doc_id].words)))
# sim_id = second_ranks[doc_id]
# print('Similar Document {}: «{}»\n'.format(sim_id, ' '.join(train_corpus[sim_id[0]].words)))

###############################################################################
# Testing the Model
# -----------------
#
# Using the same approach above, we'll infer the vector for a randomly chosen
# test document, and compare the document to our model by eye.
#

# Pick a random document from the test corpus and infer a vector from the model
# doc_id = random.randint(0, len(test_corpus) - 1)
# inferred_vector = model.infer_vector(test_corpus[doc_id])
# sims = model.dv.most_similar([inferred_vector], topn=len(model.dv))
#
# # Compare and print the most/median/least similar documents from the train corpus
# print('Test Document ({}): «{}»\n'.format(doc_id, ' '.join(test_corpus[doc_id])))
# print(u'SIMILAR/DISSIMILAR DOCS PER MODEL %s:\n' % model)
# for label, index in [('MOST', 0), ('MEDIAN', len(sims)//2), ('LEAST', len(sims) - 1)]:
#     print(u'%s %s: «%s»\n' % (label, sims[index], ' '.join(train_corpus[sims[index][0]].words)))

###############################################################################
# Conclusion
# ----------
#
# Let's review what we've seen in this tutorial:
#
# 0. Review the relevant models: bag-of-words, Word2Vec, Doc2Vec
# 1. Load and preprocess the training and test corpora (see :ref:`core_concepts_corpus`)
# 2. Train a Doc2Vec :ref:`core_concepts_model` model using the training corpus
# 3. Demonstrate how the trained model can be used to infer a :ref:`core_concepts_vector`
# 4. Assess the model
# 5. Test the model on the test corpus
#
# That's it! Doc2Vec is a great way to explore relationships between documents.
#
# Additional Resources
# --------------------
#
# If you'd like to know more about the subject matter of this tutorial, check out the links below.
#
# * `Word2Vec Paper <https://papers.nips.cc/paper/5021-distributed-representations-of-words-and-phrases-and-their-compositionality.pdf>`_
# * `Doc2Vec Paper <https://cs.stanford.edu/~quocle/paragraph_vector.pdf>`_
# * `Dr. Michael D. Lee's Website <http://faculty.sites.uci.edu/mdlee>`_
# * `Lee Corpus <http://faculty.sites.uci.edu/mdlee/similarity-data/>`__
# * `IMDB Doc2Vec Tutorial <doc2vec-IMDB.ipynb>`_
#
