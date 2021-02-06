from math import log
from gensim.models import KeyedVectors, Word2Vec


w2v: Word2Vec = KeyedVectors.load_word2vec_format(
    '200d_words.model', binary=True)

player_score = 0
com_score = 0
print('唐突だけど、連想ゲーム開始！')
t = input('最初の単語を入力してね :')
while True:
    try:
        d = w2v.most_similar(positive=[t], topn=1)
    except:
        pass
    else:
        break
    t = input('単語が辞書に載ってないよ！もう一度入力してね :')

for _ in range(100):
    d = w2v.most_similar(positive=[t], topn=1)
    print(f'→ {d[0][0]} score:{d[0][1]}')
    com_score += d[0][1]

    t = input('次の単語を入力してね :')
    try:
        s = w2v.n_similarity(t, d[0][0])
        print(f'→ {t} score:{s}')
    except:
        s = 0
        print('単語が辞書に載ってないよ！')
        t = d[0][0]
    player_score += s
print(f'player:{player_score} computer:{com_score}')
