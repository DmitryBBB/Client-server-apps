# Написать функцию host_range_ping() (возможности которой основаны на функции из примера 1)
# для перебора ip-адресов из заданного диапазона. Меняться должен только последний октет каждого адреса.
# По результатам проверки должно выводиться соответствующее сообщение.
from Data_bases_and_PyQT.Lesson_1.host_ping import check_is_ipaddress, host_ping


def host_range_ping(get_list=False):
    # Функция запрашивает начальный адрес и количество адресов
    # и если в последнес октете есть возможность увеличить адрес,
    # функция возвращает список возможных адресов
    # Затем проверяет на доступность с помощью функции host_ping из задания №1
    while True:
        # Запрашиваем начальный адрес
        start_ip = input('Введите IP адрес: ')
        try:
            ipv4_start = check_is_ipaddress(start_ip)
            # смотрим последний актет в адресе
            last_oct = int(start_ip.split('.')[3])
            break
        except Exception as e:
            print(e)
    while True:
        # запрос на количество адресов для проверки
        end_ip = input('Сколько адресов проверить: ')
        if not end_ip.isnumeric():
            print("Введите число!!!")
        else:
            # По условию меняется только последний актет
            if (last_oct + int(end_ip)) > 255+1:
                print(f'Можем менять только последний октет, '
                      f'максимальное число хостов {255+1 - last_oct}')
            else:
                break
    host_list = []
    # формируем лист IP
    [host_list.append(str(ipv4_start + x)) for x in range(int(end_ip))]
    if not get_list:
        # проверяем список(Функция из задания №1)
        host_ping(host_list)
    else:
        return host_ping(host_list, True)


if __name__ == '__main__':
    host_range_ping()
