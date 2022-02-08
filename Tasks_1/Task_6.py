# Создать текстовый файл test_file.txt, заполнить его тремя строками:
# «сетевое программирование», «сокет», «декоратор».
# Далее забыть о том, что мы сами только что создали этот файл и исходить из того,
# что перед нами файл в неизвестной кодировке. Задача: открыть этот файл БЕЗ ОШИБОК
# вне зависимости от того, в какой кодировке он был создан.6


from chardet import detect, UniversalDetector

# запись слов в тхт файл
WORDS = ['сетевое программирование', 'сокет', 'декоратор']
with open('test_file.txt', 'w') as f:
    for i in WORDS:
        f.write(f'{i}\n')
f.close()

# смотрим кодировку файла
with open("test_file.txt", 'rb') as f:
    CONTENT = f.read()
ENCODING = detect(CONTENT)['encoding']
print(ENCODING)

# открываем файл в правильной кодировке
with open("test_file.txt", encoding=ENCODING) as f:
    CONTENT = f.read()
print(CONTENT)


# with open('test_file2.txt', 'w') as f:
#     for i in WORDS:
#         f.write(f'{i}\n')
# f.close()
#
# DETECTOR = UniversalDetector()
# with open('test_file2.txt', 'rb') as text_f:
#     for i in text_f:
#         DETECTOR.feed(i)
#         if DETECTOR.done:
#             break
#     DETECTOR.close()
# print(DETECTOR.result['encoding'])
#
# with open('test_file2.txt', encoding=DETECTOR.result['encoding']) as file:
#     CONTENT =file.read()
# print(CONTENT)

