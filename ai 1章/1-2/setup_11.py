def setup():
    import os
    import urllib.request
    import zipfile
    import re
    from setup import allow_all_url
    from gensim.models import Word2Vec
    from extract_words import extract_words

    if not os.path.isfile('words.model'):
        allow_all_url()
        if not os.path.isfile('rojinto_umi.txt'):
            url = 'https://www.aozora.gr.jp/cards/001847/files/57347_ruby_57225.zip'
            name = 'aozora.zip'
            urllib.request.urlretrieve(url, name)

            with zipfile.ZipFile(name, 'r') as myzip:
                myzip.extractall()
            os.remove(name)

        with open('rojinto_umi.txt', encoding='sjis') as file:
            txt = file.read()

        txt = re.split('\-{5,}', txt)[2]
        txt = re.split('底本：', txt)[0]
        txt = txt.replace('|', '')
        txt = re.sub('《.+?》', '', txt)
        txt = re.sub('［＃.+?］', '', txt)
        txt = re.sub('\n\n', '\n', txt)
        txt = re.sub('\r', '', txt)

        sentences = extract_words(txt.split('。'))
        model = Word2Vec(sentences=sentences, iter=100)
        model.save('words.model')

        os.remove('rojinto_umi.txt')
