# Каждое из слов «class », «function», «method» записать в байтовом типе
# без преобразования в последовательность кодов (не используя методы encode и decode)
# и определить тип, содержимое и длину соответствующих переменных.2
LST_STR = ['class', 'function', 'method']

for i in LST_STR:
    byt = eval(f'b"{i}"')
    print(f'тип: {type(byt)}, {byt}, длинна {len(byt)}')
