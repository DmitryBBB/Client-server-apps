import json
import os.path
import socket
import sys
from socket import *

sys.path.append(os.path.join(os.getcwd(), '..'))
from common.utils import get_message, send_message
from common.veriables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, RESPONDEFAULT_IP_ADRESSE, \
    ERROR, MAX_CONNECTIONS, DEFAULT_PORT


# Обработка сообщений от клиентов(принимает словарь),
# проверяет корректность, возвращает словарь ответ для клиента
def process_client_message(message):
    if ACTION in message and message[ACTION] == PRESENCE and \
            TIME in message and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}

    return {
        RESPONDEFAULT_IP_ADRESSE: 400,
        ERROR: 'Bad Request'
    }


# Загрузка параметров командной строки, если параметров нет, то задаем дефолтное значение
# Сначала обрабатываем порт: server.py -p 8888 -a 127.0.0.1
def main():
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT

        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        print('После параметра -\'p\' необходимо указать номер порта')
        sys.exit(1)
    except ValueError:
        print('В качестве порта может быть указано число в диапозоне от 1024 до 65535')
        sys.exit()

    # загружаем какой адрес слушать

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''

    except IndexError:
        print('После параметра \'a\'- необходимо указать адрес который будет слушать сервер')
        sys.exit()

    # Подготовка сокета
    transport = socket(AF_INET, SOCK_STREAM)
    transport.bind((listen_address, listen_port))

    # Слушаем порт

    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        try:
            message_from_client = get_message(client)
            print(message_from_client)
            response = process_client_message(message_from_client)
            send_message(client, response)
            client.close()
        except(ValueError, json.JSONDecodeError):
            print('Получено некорректное сообщение от клиента')
            client.close()


if __name__ == '__main__':
    main()
