# Выполнить пинг веб-ресурсов yandex.ru, youtube.com
# и преобразовать результаты из байтовового в строковый тип на кириллице.5


import subprocess

args = ['ping', 'yandex.ru']
args2 = ['ping', 'youtube.com']


# subproc_ping = subprocess.Popen(args, stdout=subprocess.PIPE)
#
# for line in subproc_ping.stdout:
#     line = line.decode('cp866').encode('utf-8')
#     print(line.decode('utf-8'))

def ping_process(lst):
    subproc_ping = subprocess.Popen(lst, stdout=subprocess.PIPE)
    for line in subproc_ping.stdout:
        line = line.decode('cp866').encode('utf-8')
        print(line.decode('utf-8'))


ping_process(args)
ping_process(args2)
