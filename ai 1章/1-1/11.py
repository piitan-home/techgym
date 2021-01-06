import urllib.request
from zipfile import ZipFile
import re
import os

from janome.tokenizer import Tokenizer
from gensim.models import word2vec

from urlallow import allow_all_https

allow_all_https(show_warning=False)
# ファイルダウンロード

if os.path.isfile('11.zip'):
    url = 'https://www.aozora.gr.jp/cards/001847/files/57347_ruby_57225.zip'
    zip_ = '11.zip'
    urllib.request.urlretrieve(url, zip_)

# ダウンロードしたzipの解凍
with ZipFile(zip_) as myzip:
    myzip.extractall()
    myfile = myzip.infolist()[0]
    filename = myfile.filename
    with open(filename, encoding='sjis') as file:
        text = file.read()

text = re.split('\-{5,}', text)[2]   # ヘッダ部分の除去
text = re.split('底本：', text)[0]   # フッタ部分の除去
text = text.replace('|', '')        # | の除去
text = re.sub('《.+?》', '', text)  # ルビの削除
text = re.sub('［＃.+?］', '', text)  # 入力注の削除
text = re.sub('\n\n', '\n', text)   # 空行の削除
text = re.sub('\r', '', text)

t = Tokenizer()
obj_list = ['名詞', '動詞', '形容詞']

# テキストを引数として、形態素解析の結果で対象のみを配列で抽出する関数を定義


def extract_words(s):
    tokens = t.tokenize(s)
    r = [token.base_form for token in tokens if token.part_of_speech.split(',')[
        0] in obj_list]
    return r


# 全体のテキストを句点('。')で区切った配列
sentences = text.split('。')

# それぞれの文章を単語リストに変換(処理に数分かかります)
word_list = [extract_words(sentence) for sentence in sentences]

# 一部を確認
for word in word_list[0:3]:
    print(word)
print('\n')

# 事前準備したword_listを使ってWord2Vecの学習実施
model = word2vec.Word2Vec(word_list, size=100, min_count=5, window=5, iter=100)

# モデルのセーブ
model.save("./words.model")

# 類似している単語
sea = model.wv.most_similar('海', topn=5)
for w in sea:
    print(w[0], w[1])
print('\n')

# 類似している単語
men = model.wv.most_similar('老人', topn=5)
for w in men:
    print(w[0], w[1])
print('\n')

# コサイン類似度
ret_s = model.wv.n_similarity(['海'], ['老人'])
print(ret_s)
print('\n')

# 海から老人を引く
sea_m = model.wv.most_similar(positive=['海'], negative=['老人'], topn=5)
for w in sea_m:
    print(w[0], w[1])
print('\n')

# 海から老人を足す
sea_p = model.wv.most_similar(positive=['海', '老人'], topn=5)
for w in sea_p:
    print(w[0], w[1])
print('\n')
