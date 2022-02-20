# Тесты клиента

import sys
import os
import unittest
from pprint import pprint

pprint(sys.path)
sys.path.append(os.path.join(os.getcwd(), '..'))
from client import create_presence, process_ans
from common.veriables import TIME, ACTION, PRESENCE, USER, ACCOUNT_NAME, RESPONSE


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
        self.assertEqual(process_ans({RESPONSE: 400}), '200 : Ok')