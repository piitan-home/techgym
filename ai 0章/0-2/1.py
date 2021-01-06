from _import_ import pd, display

obj = pd.Series(['グー', 'チョキ', 'パー'])

display(obj)

display(obj[1])

display(obj.dtypes)

obj.index = ['a', 'b', 'c']
display(obj.index)
