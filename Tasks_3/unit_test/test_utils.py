import json
import os
import sys
import unittest

sys.path.append(os.path.join(os.getcwd(), '..'))

from common.utils import send_message, get_message
from common.veriables import ENCODING, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR


class TestSocket:
    # Тестовый класс для тестирования отправки и получения, при создании
    # требует словарь, который будет прогоняться через тестовую ф-ию
    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_message = None
        self.received_message = None

    def send(self, message_to_send):
        # тестовая функция отправки, корретно  кодирует сообщение,
        # так-же сохраняет что должно было отправлено в сокет.
        # message_to_send - то что отправляем в сокет
        json_test_message = json.dumps(self.test_dict)
        # кодирует сообщение
        self.encoded_message = json_test_message.encode(ENCODING)
        # сохраняем то что должно быть отправлено в сокет
        self.received_message = message_to_send

    def recv(self, max_len):
        # Получаем данные из сокета
        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode(ENCODING)


# Тестовый класс, собственно выполняющий тестирование.
class Tests(unittest.TestCase):
    test_dict_send = {
        ACTION: PRESENCE,
        TIME: 111111.111111,
        USER: {
            ACCOUNT_NAME: 'test_test'
        }
    }
    test_dict_recv_ok = {RESPONSE: 200}
    test_dict_recv_err = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

    # тестируем корректность работы фукции отправки,
    # создадим тестовый сокет и проверим корректность отправки словаря
    def test_send_message_true(self):
        # экземпляр тестового словаря, хранит собственно тестовый словарь
        test_socket = TestSocket(self.test_dict_send)
        # вызов тестируемой функции, результаты будут сохранены в тестовом сокете
        send_message(test_socket, self.test_dict_send)
        # проверка корретности кодирования словаря.
        # сравниваем результат довренного кодирования и результат от тестируемой функции
        self.assertEqual(test_socket.encoded_message, test_socket.received_message)

    def test_send_message_false(self):
        test_socket = TestSocket(self.test_dict_send)
        send_message(test_socket, self.test_dict_send)
        # проверим генерацию исключения, при не словаре на входе.
        self.assertRaises(TypeError, send_message, test_socket, 'wrong_dictionary')

    # тест функции приёма сообщения
    def test_get_message_true(self):
        test_sock_ok = TestSocket(self.test_dict_recv_ok)
        # тест корректной расшифровки корректного словаря
        self.assertEqual(get_message(test_sock_ok), self.test_dict_recv_ok)

    def test_get_message_false(self):
        test_sock_err = TestSocket(self.test_dict_recv_err)
        # тест корректной расшифровки ошибочного словаря
        self.assertEqual(get_message(test_sock_err), self.test_dict_recv_err)


if __name__ == '__main__':
    unittest.main()
