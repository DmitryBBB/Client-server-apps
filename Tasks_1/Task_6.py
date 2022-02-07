# Создать текстовый файл test_file.txt, заполнить его тремя строками:
# «сетевое программирование», «сокет», «декоратор».
# Далее забыть о том, что мы сами только что создали этот файл и исходить из того,
# что перед нами файл в неизвестной кодировке. Задача: открыть этот файл БЕЗ ОШИБОК
# вне зависимости от того, в какой кодировке он был создан.6
import locale

print(locale.getpreferredencoding())
# cp1251
words = ['сетевое программирование', 'сокет', 'декоратор']
file = open('test_file.txt', 'w')
for i in words:
    file.write(f'{i}\n')

file.close()
with open("test_file.txt", encoding='cp1251') as f:
    for line in f:
        print(line, end='')



