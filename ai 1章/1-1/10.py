from janome.tokenizer import Tokenizer
from gensim.models import word2vec

with open('techgym-AI.txt') as f:
    txt = f.read()

# 読み込んだデータを形態素解析
data = Tokenizer().tokenize(txt, wakati=True)
data = [d for d in data]

print(data)
model = word2vec.Word2Vec([data], min_count=1)
pg = model.wv.most_similar(positive=['プログラミング'], topn=5)
print(pg)
