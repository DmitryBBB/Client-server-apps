# Написать функцию host_range_ping_tab(), возможности которой основаны на функции из примера 2.
# Но в данном случае результат должен быть итоговым по всем ip-адресам, представленным в табличном формате
# (использовать модуль tabulate). Таблица должна состоять из двух колонок и выглядеть примерно так:
# Reachable
# 10.0.0.1
# 10.0.0.2
#
# Unreachable
# 10.0.0.3
# 10.0.0.4
from tabulate import tabulate

from Data_bases_and_PyQT.Lesson_1.host_range_ping import host_range_ping


def host_range_ping_tab():
    # функция объединяющяя 2 предыдущих задания, запрос диапозона IP адресов,
    # проверка их доступности
    # Используем tabulate для вывода информации в таблице
    res_dict = host_range_ping(True)  # ЗАпрашиваем хосты проверяем доступностьб получаем словарь
    print()
    print(tabulate([res_dict], headers='keys', tablefmt='pipe', stralign='center'))


if __name__ == '__main__':
    host_range_ping()
