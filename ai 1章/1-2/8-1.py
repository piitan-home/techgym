from janome.tokenizer import Tokenizer

t = Tokenizer()
print('\n'.join(map(str, t.tokenize('すもももももももものうち'))))
for token in t.tokenize('すもももももももものうち'):
    print(f'{token.part_of_speech}')
for token in t.tokenize('すもももももももものうち'):
    print(f'{token.base_form}')

