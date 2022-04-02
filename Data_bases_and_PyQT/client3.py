import argparse
import json
import logging
# Инициализация клиентского логера
import socket
import sys
import threading
import time

from common.utils import send_message, get_message
from common.veriables import ACTION, EXIT, TIME, ACCOUNT_NAME, MESSAGE, SENDER, DESTINATION, MESSAGE_TEXT, PRESENCE, \
    USER, RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from decorator import log
from errors import IncorrectDataRecivedError, ServerError, ReqFieldMissingError

logger = logging.getLogger('client_dist')


# Клас формировки и отправки сообщений и взаимодействия с пользователес
class ClientSender(threading.Thread):
    def __init__(self, account_name, sock):
        self.account_name = account_name
        self.sock = sock
        super().__init__()

    # функция создает словарь с сообщением о выходе
    def create_exit_message(self):
        return {
            ACTION: EXIT,
            TIME: time.time(),
            ACCOUNT_NAME: self.account_name
        }

    # функция запрашивает кому отправить сообщение и само сообщение
    def create_message(self):
        to = input('Введите получателя сообщения: ')
        message = input('Введите сообщения: ')
        message_dict = {
            ACTION: MESSAGE,
            SENDER: self.account_name,
            DESTINATION: to,
            TIME: time.time(),
            MESSAGE_TEXT: message
        }
        logger.debug(f'Сформирован словарь сообщения: {message_dict}')
        try:
            send_message(self.sock, message_dict)
            logger.info(f'Отправлено сообщения для пользователя: {to}')
        except:
            logger.critical(f'Потеря соединение с сервером!')
        exit(1)

    # функция взаимодействия с пользователемб запрашивает команды, отправляет сообщения
    def run(self):
        self.print_help()
        while True:
            command = input('Введите команду: ')
            if command == 'message':
                self.create_message()
            elif command == 'help':
                self.print_help()
            elif command == 'exit':
                try:
                    send_message(self.sock, self.create_exit_message())
                except:
                    pass
                print('Завершения соединения')
                logger.info('Завершение работы по команде пользователя')
                # Задержка необходимо чтобы успела выйти сообщение о выходе
                time.sleep(0.5)
                break
            else:
                print('Команда не распознана, попробуйте снова. Введите help - вывести поддерживаемы команды')

    def print_help(self):
        print('Поддерживаемые команды')
        print('message - отправить сообщение. Кому и текст будет запрошены отдельно.')
        print('help - вывести подсказки по командам')
        print('exit - выход из программы')


# Класс-приемник сообщений с сервера. Принимает сообщения, выводит в консоль
class ClientReader(threading.Thread):
    def __init__(self, account_name, sock):
        self.account_name = account_name
        self.sock = sock
        super().__init__()

    # Основной цикл приемника сообщений, принимает сообщения, выводит в консоль, завершается при потере соединения
    def run(self):
        while True:
            try:
                message = get_message(self.sock)
                if ACTION in message and message[ACTION] == MESSAGE and \
                        SENDER in message and DESTINATION in message and \
                        MESSAGE_TEXT in message and message[DESTINATION] == self.account_name:
                    print(f'\nПолучено сообщение от пользователя {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
                    logger.info(f'Получено сообщение от пользователя {message[SENDER]}:\n {message[MESSAGE_TEXT]}')
                else:
                    logger.error(f'Получено некорректное сообщение с сервера: {message}')
            except IncorrectDataRecivedError:
                logger.error('Не удалось декодировать полученное сообщение')
            except (OSError, ConnectionError, ConnectionAbortedError, ConnectionResetError, json.JSONDecodeError):
                logger.critical('Потеряно соединение с сервером!')



    # Функция генерирует запрос о присутствии клиента


@log
def create_presence(account_name):
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    logger.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
    return out


# функция разбирает ответ сервера на сообщение о присутствии, возвращает сообщение 200 если ОК, или генерирует исключение при ошибке
@log
def process_response_ans(message):
    logger.debug(f'РАзбор приветственного сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        elif message[RESPONSE] == 400:
            raise ServerError(f'400: {message[ERROR]}')
    raise ReqFieldMissingError(RESPONSE)


# парсер аргументов командной строки
@log
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_name = namespace.name
    # проверим подходящий номер порта
    if not 1023 < server_port < 65536:
        logger.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}'
        )
    exit(1)
    return server_address, server_port, client_name


def main():
    # Сообщаем о запуске
    print('Консольный месседжер. Клиентский модуль')

    # Загружаем параметры командной строки
    server_address, server_port, client_name = arg_parser()

    # Если имя пользователя не было задано, необходимо запросить пользователя
    if not client_name:
        client_name = input('Введите имя пользователя: ')
    else:
        print(f'Клиентский модуль запущен с именем {client_name}')

    logger.info(f'запущен клиент с параметрами: адрес сервера {server_address}, '
              f'порт: {server_port}, имя пользователя: {client_name}')

    # инициализация сокета и сообщение серверу о нашем появлении
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        send_message(transport, create_presence(client_name))
        answer = process_response_ans(get_message(transport))
        logger.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')
        print('Установлено соединение с сервером')

    except json.JSONDecodeError:
        logger.error('Не удалось декодировать полученную Json строку')
        exit(1)
    except ServerError as error:
        logger.error(f'При установки соединения сервер вернул ошибку: {error.text}')
        exit(1)
    except ReqFieldMissingError as missing_error:
        logger.error(f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
        exit(1)
    except (ConnectionRefusedError, ConnectionError):
        logger.critical(
            f'Не удалось подключиться к серверу {server_address}:{server_port}, '
            f'конечный компьютер отверг запрос на подключение'
        )
        exit(1)
    else:
        # Если соединение с сервером установлено корректно, запускаем клиентский процесс приема сообщений
        module_reciver = ClientReader(client_name, transport)
        module_reciver.daemon = True
        module_reciver.start()

        # затем запускаем отправку сообщений и взамодействие с пользователем
        module_sender = ClientSender(client_name, transport)
        module_sender.daemon = True
        module_sender.start()
        logger.debug('Запущены процессы')

        # Watchdog основной цикл, если один из потоков завершён, то значит или потеряно соединение, или пользователь
        # ввёл exit. Поскольку все события обработываются в потоках, достаточно просто завершить цикл.
        while True:
            time.sleep(1)
            if module_sender.is_alive() and module_reciver.is_alive():
                continue
            break

if __name__ == '__main__':
    main()