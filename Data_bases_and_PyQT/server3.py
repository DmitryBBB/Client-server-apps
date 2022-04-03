import argparse
import logging
import select
import socket

from Data_bases_and_PyQT.descriptrs import Port
from Data_bases_and_PyQT.metaclasses import ServerMaker
from common.utils import *
from common.veriables import DEFAULT_PORT, DESTINATION, SENDER, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE_200, RESPONSE_400, ERROR, MESSAGE, MESSAGE_TEXT, EXIT
from decorator import log

# Инициализация логирования сервера
logger = logging.getLogger('server_dist')


# Парсер аргументов командной строки
@log
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p
    return listen_address, listen_port


# Основной класс cервера
class Server(metaclass=ServerMaker):
    port = Port()

    def __init__(self, listen_address, listen_port):
        # параметры подключения
        self.addr = listen_address
        self.port = listen_port

        # Список подключенных клиентов
        self.clients = []
        # Список сообщений на отправку
        self.messages = []
        # словар содержащий сопоставленные имена и соответствующие им сокеты
        self.names = dict()

    def init_socket(self):
        logger.info(
            f'Запущен сервер, порт для подключения: {self.port}, '
            f'адресс с которого принимаются подключения: {self.addr} '
            f'Если адресс не указан принимаются соединения с любых адресов'
        )

        # Готовим сокет
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.bind((self.addr, self.port))
        transport.settimeout(0.5)

        # Начинаем слушать сокет
        self.sock = transport
        self.sock.listen()

    def main_loop(self):
        # Инициализация сокета
        self.init_socket()

        # основной цикл программы сервера
        while True:
            # ждем подключения, если таймаут вышел ловим исключение
            try:
                client, client_address = self.sock.accept()
            except OSError:
                pass
            else:
                logger.info(f'Установлено соединение с ПК {client_address}')
                self.clients.append(client)

            recv_data_lst = []
            send_data_lst = []
            err_lst = []

            # Проверяем на наличие ждущих клиентов
            try:
                if self.clients:
                    recv_data_lst, send_data_lst, err_lst = select.select(self.clients, self.clients, [], 0)
            except OSError:
                pass

            # проверяем сообщения и если ошибка исключаем клиента
            if recv_data_lst:
                for client_with_message in recv_data_lst:
                    try:
                        self.process_client_message(get_message(client_with_message), client_with_message)
                    except:
                        logger.info(
                            f'Клиент {client_with_message.getpeername()} отключился от сервера '
                        )
                        self.clients.remove(client_with_message)

            # Если есть сообщения обрабатываем каждое
            for message in self.messages:
                try:
                    self.process_message(message, send_data_lst)
                except Exception as e:
                    logger.info(
                        f'Связь с клиентом с именем {message[DESTINATION]} была потеряна, '
                        f'ошибка {e}'
                    )
                    self.clients.remove(self.names[message[DESTINATION]])
                    del self.names[message[DESTINATION]]
            self.messages.clear()

        # Функция адресной отправки сообщения определенному клиенту
        # принимает словарь-сообщение, список зарегестрированных пользователей
        # и слушает сокеты. Ничего не возвращает

    def process_message(self, message, listen_sock):
        if message[DESTINATION] in self.names and \
                self.names[message[DESTINATION]] in listen_sock:
            send_message(self.names[message[DESTINATION]], message)
            logger.info(
                f'Отправлено сообщение пользователю {message[DESTINATION]} '
                f'от пользователя {message[SENDER]}'
            )
        elif message[DESTINATION] in self.names \
                and self.names[message[DESTINATION]] not in listen_sock:
            raise ConnectionError
        else:
            logger.error(
                f'Пользователь  {message[DESTINATION]} не зарегестрирован на сервере '
                f'отправка сообщения невозможна'
            )

    # Обработчик сообщений от клиентов, принимает словарь - сообщение от клиента,
    # проверяет корректность, отправляет словарь ответ в случае необходимости
    def process_client_message(self, message, client):
        logger.debug(f'Разбор сообщения от клиента: {message}')
        # Если это сообщение о присутствии, принимаем и отвечаем
        if ACTION in message and message[ACTION] == PRESENCE \
                and TIME in message and USER in message:
            # Если такой пользователь еще не зарегестрирован, регистрируем,
            # иначе отправляем ответ и завершаем соединение
            if message[USER][ACCOUNT_NAME] not in self.names.keys():
                self.names[message[USER][ACCOUNT_NAME]] = client
                send_message(client, RESPONSE_200)
            else:
                response = RESPONSE_400
                response[ERROR] = 'Имя пользователя уже занято'
                send_message(client, response)
                self.clients.remove(client)
                client.close()
            return
        # Если это сообщение добавляем его в очередь сообщений. Ответ не требуется
        elif ACTION in message and message[ACTION] == MESSAGE \
                and DESTINATION in message and TIME in message \
                and SENDER in message and MESSAGE_TEXT in message:
            self.messages.append(message)
            return
            # Если клиент выходит
        elif ACTION in message and message[ACTION] == EXIT \
                and ACCOUNT_NAME in message:
            self.clients.remove(self.names[ACCOUNT_NAME])
            self.names[ACCOUNT_NAME].close()
            del self.names[ACCOUNT_NAME]
            return
        # Иначе отдаем BAD request
        else:
            response = RESPONSE_400
            response[ERROR] = 'Запрос не корректен'
            send_message(client, response)
            return


def main():
    # Загрузка параметров командной строки, если нет параметров,
    # то задаём значения по умолчанию.
    listen_address, listen_port = arg_parser()

    # Создание экземпляра класса - сервера.
    server = Server(listen_address, listen_port)
    server.main_loop()


if __name__ == '__main__':
    main()
