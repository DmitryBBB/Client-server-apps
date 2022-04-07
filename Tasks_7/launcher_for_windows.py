# Служебный скрипт запуска/остановки нескольких клиентских приложений
from subprocess import Popen, CREATE_NEW_CONSOLE

P_LIST = []

while True:
    USER = input('Запустить 10 клиентов (s)/ Закрыть клиентов (x)/ Выйти (q)')

    if USER == 'q':
        break

    elif USER == 's':
        for i in range(10):
            P_LIST.append(Popen('python client1.py', creationflags=CREATE_NEW_CONSOLE))

        print('Запущено 10 клиентов')
    elif USER == 'x':
            for p in P_LIST:
                p.kill()
            P_LIST.clear()