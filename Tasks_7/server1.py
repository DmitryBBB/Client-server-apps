import argparse
import logging
import select
import sys
import time
from socket import socket, AF_INET, SOCK_STREAM

from common.utils import send_message, get_message
from common.veriables import ACTION, PRESENCE, TIME, USER, RESPONSE, ACCOUNT_NAME, ERROR, DEFAULT_PORT, MAX_CONNECTIONS, \
    MESSAGE, MESSAGE_TEXT, SENDER
from decorator import log

LOGGER = logging.getLogger('server')


@log
def process_client_message(message, messages_list, client):
    # Обработчик сообщений от клиентов, принимает словарь
    # - сообщение от клиента, проверяет корректность, отправляет
    # словарь ответ для клиента с результатом приема

    LOGGER.debug(f'Разбор сообщения от клиента: {message}')
    # Сообщение о присутствии, принимаем и отвечаем если успех
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        send_message(client, {RESPONSE: 200})
        return
    # Если это сообщение добавляем его в очередь сообщений. ответ не требуетсяю
    elif ACTION in message and message[ACTION] == MESSAGE and TIME in message and \
            MESSAGE_TEXT in message:
        messages_list.append(message[ACCOUNT_NAME], message[MESSAGE_TEXT])
        return
    # Иначе отдаем BAD request
    else:
        send_message(client, {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        })
        return


@log
def arg_parser():
    # Парсер аргументов командной строки
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    if not 1023 < listen_port < 65536:
        LOGGER.critical(
            f'Попытка запуска сервера с указанием неподходящего порта '
            f'{listen_port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)



    return listen_address, listen_port


def main():
    # Загрузка параметров командной строки, если нет, значение по умолчанию
    listen_address, listen_port = arg_parser()

    LOGGER.info(f'Запущен сервер, порт для подключений - {listen_port},'
                f'Адрес с которого принимаются подключения - {listen_address}'
                f'Если адрес не указан принимаются соединения с любых адресов')

    transport = socket(AF_INET, SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    transport.settimeout(0.5)

    # Список клиентов, очередь сообщений
    clients = []
    messages = []

    # слушаем порт
    transport.listen(MAX_CONNECTIONS)
    # ОСновной цикл сервера
    while True:
        # Ждем подключения, если таймаут вышел, ловим исключение
        try:
            client, client_address = transport.accept()
        except OSError as err:
            print(err.errno)
            pass
        else:
            LOGGER.info(f'Установлено соединение с ПК {client_address}')
            clients.append(client)

        recv_data_lst = []
        send_data_lst = []
        err_lst = []

        # Проверяем на наличие ждущих клиентов
        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select \
                    (clients, clients, [], 0)
        except OSError:
            pass

        # принимаем сообщения и если там есть
        # сообщения, кладем в словарь, если ошибка, исключаем клиента
        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    process_client_message(get_message(client_with_message),
                                           messages, client_with_message)
                except:
                    LOGGER.info(f'Клиент {client_with_message.getpeername()} '
                                f'отключился от сервера')
                    clients.remove(client_with_message)

        # Если есть сообщения для отправки и ожидающие клиенты,
        # отправляем им сообщение
        if messages and send_data_lst:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1]
            }
            del messages[0]
            for waiting_client in send_data_lst:
                try:
                    send_message(waiting_client, message)
                except:
                    LOGGER.info(f'Клиент {waiting_client.getpeername()} отключился '
                                f'от сервера.')
                    waiting_client.close()
                    clients.remove(waiting_client)


if __name__ == '__main__':
    main()