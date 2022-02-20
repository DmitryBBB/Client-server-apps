import json
import os
import sys
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from common.utils import send_message, get_message
from common.veriables import ENCODING, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR


class TestSocket:
    # Тестовый класс для тестирования отправки и получения,
    # при создании требуется словарь, который будет прогонятся
    # через тестовый словарь
    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_message = None
        self.received_message = None


    def send(self, message_to_send):
        # Тестовая ф-ия отправкиб корректно кодирует сообщение
        # так-же сохраняет то, что должно быть отправлено в сокет.
        # message_to_send - то, что отправляем в сокет
        json_test_message = json.dumps(self.test_dict)
        # кодируем сообщение
        self.encoded_message = json_test_message.encode(ENCODING)
        # сохраняем то что должно быть отправлено в сокет
        self.received_message = message_to_send


    def recv(self, max_len):
        # Получаем данные из сокета
        json_test_message = json.dumps(self.test_dict)
        return json_test_message

class TestUtils(unittest.TestCase):
    # Тестовый класс выполняющий тестирование

    test_dict_send = {
        ACTION: PRESENCE,
        TIME: 111111.111111,
        USER: {
            ACCOUNT_NAME: 'test'
        }
    }

    test_dict_recv_ok = {RESPONSE: 200}
    test_dict_recv_err = {
        RESPONSE: 400,
        ERROR: 'BAD Request'
    }

    def test_send_message(self):
        # Тестируем функцию отправки, создадим
        # тестовый сокет и проверим корректность отправки словаря

        # Экземпляр тестового словаря
        test_socket = TestSocket(self.test_dict_send)
        # вызов тестируемой ф-ции, результаты будут сохранены в тестовом сокете
        send_message(test_socket, self.test_dict_send)
        # Проверка корректности кодирования словаря
        # Сравниваем результат кодирования
        self.assertEqual(test_socket.encoded_message, test_socket.received_message)
        self.assertRaises(TypeError, send_message, test_socket, 'wrong_dictionary')

    def test_get_message(self):
        # Тест функции приема сообщения
        test_sock_ok = TestSocket(self.test_dict_recv_ok)
        test_sock_err = TestSocket(self.test_dict_recv_err)
        # тест корректной расшифровки корректного словаря
        self.assertEqual(get_message(test_sock_ok), self.test_dict_recv_ok)
        # тест корректной расшифровки ошибочного словаря
        self.assertEqual(get_message(test_sock_err), self.test_dict_recv_err)

if __name__ == '__main__':
    unittest.main()