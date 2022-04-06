# В основе метода библиотеки dis - анализ кода с помощью его дизассемблирования
# (разбор кода на составляющие: в нашем случае - на атрибуты и методы класса)
# https://docs.python.org/3/library/dis.html

import dis
from pprint import pprint


# Metaclass для проверки соответствия сервера
class ServerMaker(type):
    def __init__(cls, clsname, bases, clsdict):
        # clsname - экземпляр метакласса - Server
        # bases - кортеж базовых классов
        # clsdict - словарь атрибутов и методов экземпляра метакласса

        # список методов, которые используются в функциях класса
        # Получаем с помощью LOAD_GLOBAL
        methods = []
        # Обычно методы, обёрнутые декораторами попадают не в 'LOAD_GLOBAL', а в 'LOAD_METHOD'
        # Получаем с помощью LOAD_METHOD
        methods_2 = []
        # Атрибуты используемые в функциях классов
        # Получаем с помощью LOAD_ATTR
        attrs = []

        # перебираем ключи
        for func in clsdict:
            try:
                # возвращаем итератор по инструкции в представленной функции, методе, строке исходного кода или объекте кода
                ret = dis.get_instructions(clsdict[func])
                # Если не функция то ловим исключение
                # (если порт)
            except TypeError:
                pass
            else:
                # раз функция разбираем код получая используемы методы и атрибуты
                for i in ret:
                    # print(i)
                    # i - Instruction
                    # argrepr = 'send_message'
                    # opname - имя для операции

                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            # заполняем список методами, использующимися в функциях класса
                            methods.append(i.argval)
                    elif i.opname == 'LOAD_METHOD':
                        if i.argval not in methods_2:
                            # заполняем список атрибутами, использующимися в функциях класса
                            methods_2.append(i.argval)
                    elif i.opname == 'LOAD_ATTR':
                        if i.argval not in attrs:
                            # заполняем список атрибутами, использующимися в функциях класса
                            attrs.append(i.argval)

        # print('methods', '_' * 20)
        # pprint(methods)
        # print('methods_2', '_' * 20)
        # pprint(methods_2)
        # print('attrs', '_' * 20)
        # pprint(attrs)

        # если обнаружено использование недопустимого метода connect, вызываем исключение
        if 'connect' in methods:
            raise TypeError('Недопустимо использование метода connect в серверном классе')
        # если сокет не инициализировался константами SOCK_STREAM(TCP) AF_INET(IPv4), тоже исключение
        if not ('SOCK_STREAM' in attrs and 'AF_INET' in attrs):
            raise TypeError('Некорректная инициализация сокета')
        # Обязательно вызываем конструктор предка
        super().__init__(clsname, bases, clsdict)


# Metaclass для проверки корректности клиентов

class ClientMaker(type):
    def __init__(cls, clsname, bases, clsdict):
        methods = []
        for func in clsdict:
            try:
                # возвращаем итератор по инструкции в представленной функции, методе, строке исходного кода или объекте кода
                ret = dis.get_instructions(clsdict[func])
                # Если не функция то ловим исключение
                # (если порт)
            except TypeError:
                pass
            else:
                # раз функция разбираем код получая используемы методы и атрибуты
                for i in ret:

                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                        # заполняем список методами, использующимися в функциях класса
                            methods.append(i.argval)

        # Если обнаружено использование недопустимого метода accept, listen, socket бросаем исключение
        for command in ('accept', 'listen', 'socket'):
            if command in methods:
                raise TypeError('В классе используется запрещенный метод')
        if 'get_message' in methods or 'send_message' in methods:
            pass
        else:
            raise TypeError('Отсутствуют вызовы функций, работающих с сокетами')
        super().__init__(clsname, bases, clsdict)
