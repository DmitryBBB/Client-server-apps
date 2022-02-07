# Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать
# в байтовом типе. Важно: решение должно быть универсальным, т.е. не зависеть от того,
# какие конкретно слова мы исследуем.3


LST_STR = ['attribute', 'класс', 'функция', 'type']


def conversion_to_bytes(lst):
    for i in lst:
        j = bytes(i, encoding='utf-8')
        print(f'тип: {type(j)}, {j}')


conversion_to_bytes(LST_STR)


