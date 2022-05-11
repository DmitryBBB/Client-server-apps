# Тесты сервера
import os
import sys
import unittest
from pprint import pprint

sys.path.append(os.path.join(os.getcwd(), '..'))
pprint(sys.path)
from common.veriables import RESPONSE, ERROR, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME
from server import process_client_message


class TestServer(unittest.TestCase):
    err_dict = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }
    ok_dict = {RESPONSE: 200}

    def test_ok_check(self):
        # Корректный запрос
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}}), self.ok_dict
        )

    def test_no_action(self):
        # Ошибка если нет действия
        self.assertEqual(process_client_message(
            {TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict
        )

    def test_wrong_action(self):
        # Ошибка если действие неизвестно
        self.assertEqual(process_client_message(
            {ACTION: 'Wrong', TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict
        )

    def test_no_time(self):
        # Ошибка если запрос не содержит штампа времени
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict
        )

    def test_no_user(self):
        # Ошибка если нет юзера
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: '1.1'}), self.err_dict
        )

    def test_unknown_user(self):
        # Ошибка если не Guest
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest1'}}), self.err_dict
        )


if __name__ == '__main__':
    unittest.main()
