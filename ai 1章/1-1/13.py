from gensim.models import KeyedVectors
import os
import urllib.request
from urlallow import allow_all_https

allow_all_https(show_warning=False)

title = "stanby-jobs-200d-word2vector.bin"
if not os.path.exists(title):
    print(title + " DOWNLOAD.")
    url = "https://github.com/bizreach/ai/releases/download/2018-03-13/stanby-jobs-200d-word2vector.bin"
    urllib.request.urlretrieve(url, "{0}".format(title))
else:
    print(title + " EXIST.")

# ダウンロード先のパスを指定
MODEL_FILENAME = "./stanby-jobs-200d-word2vector.bin"
w2v = KeyedVectors.load_word2vec_format(MODEL_FILENAME, binary=True)

# 計算した結果近い単語が出てくる
print("「テクノロジー」")
words = w2v.most_similar(positive=['テクノロジー'], topn=5)
for word in words:
    print(word)
print('\n')

print("「テクノロジー」+「金融」")
words = w2v.most_similar(positive=['テクノロジー', '金融'], topn=5)
for word in words:
    print(word)
print('\n')

print("「テクノロジー」+「金融」-「IT」")
words = w2v.most_similar(positive=['テクノロジー', '金融'], negative=['IT'], topn=5)
for word in words:
    print(word)
print('\n')

print("Java")
words = w2v.most_similar(positive=['Java'], topn=5)
for word in words:
    print(word)
print('\n')

print('「Java」と「PHP」のコサイン類似度')
ret = w2v.n_similarity(['Java'], ['PHP'])
print(ret)
