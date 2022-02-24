"""Константы"""

# Порт по умолчанию для сетевого взаимодействия
import logging

DEFAULT_PORT = 7777
# IP адрес по умолчанию для подкл. клиента
DEFAULT_IP_ADDRESS = '127.0.0.1'
# Максимальная очередь подключений
MAX_CONNECTIONS = 5
# Максимальная длинна сообщения в байтах
MAX_PACKAGE_LENGTH = 1024
# Кодировка проекта
ENCODING = 'utf-8'

# Текущий уровень логирования
LOGGING_LEVEL = logging.DEBUG

# Основные ключи протокола JIM:

ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'

# Прощие ключи JIM:
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
RESPONDEFAULT_IP_ADRESSE = 'response'
