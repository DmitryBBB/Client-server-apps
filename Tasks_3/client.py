import argparse
import json
import logging
import os
import socket
import sys
import time

sys.path.append(os.path.join(os.getcwd(), '..'))
from errors import ReqFieldMissingError
from common.utils import get_message, send_message
from common.veriables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_PORT, \
    DEFAULT_IP_ADDRESS

CLIENT_LOGGER = logging.getLogger('client')


def create_presence(account_name='Guest'):
    # Функция создает запрос о присутствие клиента

    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    CLIENT_LOGGER.debug(f'Сформировано {PRESENCE} сообщения для пользователя {account_name}')
    return out


def process_ans(message):
    # Функция разбирает ответ сервера
    CLIENT_LOGGER.debug(f'Разбор сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : Ok'
        return f'400 : {message[ERROR]}'
    raise ReqFieldMissingError(RESPONSE)


def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    return parser


def main():
    # Загружаем параметры коммандной строки
    parser = create_arg_parser()
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port

    if not 1024 < server_port < 65535:
        CLIENT_LOGGER.critical(f'Попытка запуска клиента с неподходящим номером порта: {server_port}'
                               f'Допустимы адреса от 1024 до 65535. Клиент завершается')
        sys.exit(1)
    CLIENT_LOGGER.info(f'Запущен клиент с параметрами '
                       f'адрес сервера: {server_address}, порт: {server_port}')

    # инициализация сокета и обмен
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        message_to_server = create_presence()
        send_message(transport, message_to_server)
        answer = process_ans(get_message(transport))
        CLIENT_LOGGER.info(f'Принят ответ от сервера {answer}')
        print(answer)
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать полученную Json строку')
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f'Не удалось подключится к серверу {server_address} : {server_port}'
                               f' конечный компльютер отверг запрос на подключение')
    except ReqFieldMissingError as missing_error:
        CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле'
                            f' {missing_error.missing_field}')


if __name__ == '__main__':
    main()
