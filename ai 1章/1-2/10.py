from gensim.models import Word2Vec
from janome.tokenizer import Tokenizer


with open('techgym-AI.txt') as f:
    txt = f.read()
t = Tokenizer()
sentences = [list(t.tokenize(t_, wakati=True)) for t_ in txt.split('\r\n')]
model = Word2Vec(sentences=sentences, min_count=1, iter=10)

print(model.wv['プログラミング'])
print(model.most_similar(positive=['プログラミング'], topn=5))
