# Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать
# в байтовом типе. Важно: решение должно быть универсальным, т.е. не зависеть от того,
# какие конкретно слова мы исследуем.3


LST_STR = ['attribute', 'класс', 'функция', 'type']


# Вариант 1
def conversion_to_bytes(lst):
    for i in lst:
        try:
            i.encode('ascii')
            print(f'тип: {type(i)}, {i}')
        except UnicodeEncodeError:
            print(f' Слово {i} невозможно записать в виде байтовой строки')


conversion_to_bytes(LST_STR)
print('_________________________')
# Вариант 2

for i in LST_STR:
    try:
        word_bytes = f'b"{i}"'
        eval(word_bytes)
    except SyntaxError:
        print(f' Слово {i} невозможно записать в виде байтовой строки')
print('_________________________')

# Вариант 3
for i in LST_STR:
    if not i.isascii():
        print(f' Слово {i} невозможно записать в виде байтовой строки')
