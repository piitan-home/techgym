from gensim.models import Word2Vec

#モデル
sentences = [["猫", "鳴く", "にゃー"], ["犬", "鳴く", "わんわん"]]
model = Word2Vec(sentences, min_count=1)

vector = model.wv['猫']
cat = model.wv.most_similar(positive=['猫'])

print(cat)
ret_s = model.wv.n_similarity(['犬'],['猫']) 
print(ret_s)