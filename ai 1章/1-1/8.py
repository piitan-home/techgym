
from janome.tokenizer import Tokenizer

with open('techgym-AI.txt') as f:
    txt = f.read()

t = Tokenizer()
tokens = t.tokenize(txt, wakati=True)
print([t for t in tokens])
