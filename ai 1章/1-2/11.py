from gensim.models import Word2Vec
from setup_11 import setup

setup()
model = Word2Vec.load('words.model')

print(model.wv.most_similar(positive=['老人'], topn=5))
print(model.wv.most_similar(positive=['海'], topn=5))
print(model.wv.most_similar(positive=['海'], negative=['老人'], topn=5))
print(model.wv.most_similar(positive=['老人', '海'], topn=5))
