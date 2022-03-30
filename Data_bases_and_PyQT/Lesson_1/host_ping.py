# Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться доступность сетевых узлов.
# Аргументом функции является список, в котором каждый сетевой узел должен быть представлен именем хоста или ip-адресом.
# В функции необходимо перебирать ip-адреса и проверять их доступность с выводом соответствующего сообщения
# («Узел доступен», «Узел недоступен»). При этом ip-адрес сетевого узла должен создаваться с помощью функции ip_address().
# (Внимание! Аргументом сабпроцеса должен быть список, а не строка!!! Крайне желательно использование потоков.)
import os
import platform
import subprocess
import threading
import time
from ipaddress import ip_address
from pprint import pprint

# словарь с результатами
from tabulate import tabulate

result = {'Доступные узлы': "", "Недоступные узлы": ""}

# заглушка, чтобы поток не выводился на экран
DNULL = open(os.devnull, 'w')


def check_is_ipaddress(value):
    # Функция проверки IP адреса на корректность, если ок возвращает его
    try:
        ipv4 = ip_address(value)
    except ValueError:
        raise Exception('Некорректный IP адрес')
    return ipv4





def ping(ipv4, result, get_list):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    response = subprocess.Popen(['ping', param, '1', '-w', '1', str(ipv4)], stdout=subprocess.PIPE)
    if response.wait() == 0:
        result['Доступные узлы'] += f'{ipv4}\n'
        res_string = f'{ipv4} - Узел доступен'
        if not get_list:
            print(res_string)
        return res_string
    else:
        result['Недоступные узлы'] += f'{ipv4}\n'
        res_string = f'{ipv4} - Узел недоступен'
        if not get_list:
        # Если результат не нужно добавлять в словарь выводим на экран
            print(res_string)
        return res_string

def host_ping(hosts_list, get_list=False):
    # Функция проверки доступности хостов
    # hosts_list - список хостов
    # get_list - признак того нужно ли отдать результат в виде словаря
    print('Начинаю проверку доступности узлов')
    threads = []
    for host in hosts_list:
        # проверяем IP адрес на корректность
        try:
            ipv4 = check_is_ipaddress(host)
        except Exception as e:
            print(f'{host} - {e} воспринимаю как доменное имя')
            ipv4 = host
        thread = threading.Thread(target=ping, args=(ipv4, result, get_list))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    if get_list:
    # Если нужно вернуть словарь, возвращаем(задача 3)
        return result

if __name__ == '__main__':
    # список проверяемых хостов
    hosts_list = ['192.168.1.1', '127.0.0.1', 'youtube.com', 'mail.ru',
                  '0.0.0.1', '0.0.0.2', '0.0.0.3', '0.0.0.4', '0.0.0.5',
                  '0.0.0.6', '0.0.0.7', '0.0.0.8', '0.0.0.9', '0.0.1.0']
    start = time.time()
    host_ping(hosts_list)
    end = time.time()
    print(f'total time: {int(end - start)}')
    # pprint(result)
