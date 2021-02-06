
from gensim.models import KeyedVectors, Word2Vec
from IPython.display import display

model: Word2Vec = KeyedVectors.load_word2vec_format(
    '200d_words.model', binary=True)
display(model.most_similar(positive=['テクノロジー'], topn=5))
display(model.most_similar(positive=['テクノロジー', '金融'], topn=5))
display(model.most_similar(positive=['テクノロジー', '金融'], negative=['IT'], topn=5))

display(model.n_similarity('Java', 'PHP'))
