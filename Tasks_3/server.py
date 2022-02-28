import argparse
import json
import logging
import os.path
import socket
import sys
from socket import *

from decorator import log
from errors import IncorrectDataRecivedError

sys.path.append(os.path.join(os.getcwd(), '..'))
from common.utils import get_message, send_message
from common.veriables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, \
    DEFAULT_PORT, MAX_CONNECTIONS

# Инициализация логирования сервера
SERVER_LOGGER = logging.getLogger('server')


# Обработка сообщений от клиентов(принимает словарь),
# проверяет корректность, возвращает словарь ответ для клиента
@log
def process_client_message(message):
    if ACTION in message and message[ACTION] == PRESENCE and \
            TIME in message and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}

    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

@log
def create_arg_parser():
    # Парсер аргументов командной строки
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    return parser


# Загрузка параметров командной строки, если параметров нет, то задаем дефолтное значение

def main():
    parser = create_arg_parser()
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    if not 1024 < listen_port > 65535:
        SERVER_LOGGER.critical(f'Попытка запуска сервера с указанием'
                               f' {listen_port} не подходящего порта'
                               f' Допустимы адреса 1024 до 65535')
        sys.exit(1)
    SERVER_LOGGER.info(f'Запущен сервер, порт для подключений {listen_port},'
                       f'Адрес с которого принимаются подключения {listen_address}'
                       f'Если адрес не указан принимаются соединения с любых адресов')

    # загружаем какой адрес слушать

    # try:
    #     if '-a' in sys.argv:
    #         listen_address = sys.argv[sys.argv.index('-a') + 1]
    #     else:
    #         listen_address = ''
    #
    # except IndexError:
    #     print('После параметра \'a\'- необходимо указать адрес который будет слушать сервер')
    #     sys.exit()

    # Подготовка сокета
    transport = socket(AF_INET, SOCK_STREAM)
    transport.bind((listen_address, listen_port))

    # Слушаем порт

    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        SERVER_LOGGER.info(f'Установлено соединение с ПК {client_address}')
        try:
            message_from_client = get_message(client)
            SERVER_LOGGER.debug(f'Получено сообщение {message_from_client}')
            response = process_client_message(message_from_client)
            SERVER_LOGGER.info(f'Сформироват ответ клиенту {response}')
            send_message(client, response)
            SERVER_LOGGER.debug(f'Соединение с клиентом закрыто {client_address}')
            client.close()
        except json.JSONDecodeError:
            SERVER_LOGGER.error(f'Не удалось декодировать Json строку, полученную от'
                                f' клиента {client_address}, соединение закрывается')
            client.close()
        except IncorrectDataRecivedError:
            SERVER_LOGGER.error(f'От клиента {client_address} приняты некорректные'
                                f' данные, соединение закрывается')
            client.close()


if __name__ == '__main__':
    main()
