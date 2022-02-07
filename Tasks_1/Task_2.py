# Каждое из слов «class », «function», «method» записать в байтовом типе
# без преобразования в последовательность кодов (не используя методы encode и decode)
# и определить тип, содержимое и длину соответствующих переменных.
LST_STR = ['class', 'function', 'method']


def conversion_to_bytes(lst):
    for i in lst:
        j = bytes(i, encoding='utf-8')
        print(f'тип: {type(j)}, {j}, длинна {len(j)}')


conversion_to_bytes(LST_STR)
