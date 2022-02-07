# Преобразовать слова «разработка», «администрирование», «protocol», «standard»
# из строкового представления в байтовое и выполнить обратное преобразование
# (используя методы encode и decode).


LST_STR = ['разработка', 'администрирование', 'protocol', 'standard']


def conversion_to_bytes_and_back(lst):
    LST_BYTES = [i.encode(encoding='utf-8') for i in lst]
    print(LST_BYTES)
    LST_STR = [i.decode('utf-8') for i in LST_BYTES]
    print(LST_STR)


conversion_to_bytes_and_back(LST_STR)
