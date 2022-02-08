# Выполнить пинг веб-ресурсов yandex.ru, youtube.com
# и преобразовать результаты из байтовового в строковый тип на кириллице.5

import subprocess

import chardet

args_lst = ['yandex.ru', 'youtube.com']

args2 = 'yandex.ru'
args1 = 'youtube.com'


# def ping_web(ping_list):
#     param = '-n' if platform.system().lower() == 'windows' else '-c'
#     for args in ping_list:
#         args = ['ping', param, '2', args]
#         result = subprocess.Popen(args, stdout=subprocess.PIPE)
#         for line in result.stdout:
#             result = chardet.detect(line)
#             print(f'result: {result}')
#             line = line.decode(result['encoding']).encode('utf-8')
#             print(line.decode('utf-8'))
#         print('---------------------------------------')
#
#
# ping_web(args_lst)


def ping_service(link):
    args = ['ping', link]
    ping = subprocess.Popen(args, stdout=subprocess.PIPE)
    count = 0
    for line in ping.stdout:
        result = chardet.detect(line)
        line = line.decode(result['encoding']).encode('utf-8')
        print(line.decode('utf-8'))
        if count == 4:
            break
        count += 1


ping_service(args2)
ping_service(args1)
