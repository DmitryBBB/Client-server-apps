# Тесты клиента

import os
import sys
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from client import create_presence, process_ans
from common.veriables import TIME, ACTION, PRESENCE, USER, ACCOUNT_NAME, RESPONSE, ERROR


class TestClass(unittest.TestCase):

    def test_def_presense(self):
        # Тест корректного запроса
        test = create_presence()
        test[TIME] = 1.1
        # Время необходимо приравнять принудительно иначе тест
        # никогда не будет пройден
        self.assertEqual(test, {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}})

    def test_200_ans(self):
        # Тест корректного разбора ответа 200
        self.assertEqual(process_ans({RESPONSE: 200}), '200 : Ok')

    def test_400_ans(self):
        # Тест корректного разбора ответа
        self.assertEqual(process_ans({RESPONSE: 400, ERROR: 'Bad Request'}), '400 : Bad Request')

    def test_no_response(self):
        # Тест исключения без поля респонсе
        self.assertRaises(ValueError, process_ans, {ERROR: 'Bad Request'})


if __name__ == '__main__':
    unittest.main()