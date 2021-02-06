from janome.tokenizer import Tokenizer

t = Tokenizer()
with open('techgym-AI.txt') as f:
    txt = f.read()
txt = ''.join(txt.split())

print('\n'.join(map(str, t.tokenize(txt))))
