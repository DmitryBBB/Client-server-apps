import json

from Data_bases_and_PyQT.common.decorator import log
from Data_bases_and_PyQT.common.veriables import *

"""Утилита приёма и декодирования сообщения
принимает байты выдаёт словарь, если приняточто-то другое отдаёт ошибку
"""


@log
def get_message(client):
    encoded_response = client.recv(MAX_PACKAGE_LENGTH)
    json_response = encoded_response.decode(ENCODING)
    response = json.loads(json_response)
    if isinstance(response, dict):
        return response
    else:
        raise TypeError


"""Утилита кодирования и отправки сообщения
принимает словарь и отправляет его
"""


@log
def send_message(sock, message):
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)
