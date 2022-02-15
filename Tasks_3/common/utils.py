import json

from Tasks_3.common.veriables import MAX_PACKAGE_LENGTH, ENCODING


def get_message(client):
    # Утилита приема и декодирования сообщения(принимает байты выдает словарь,
    # так же выдает ошибку если передано что-то другое)
    encoded_response = client.recv(MAX_PACKAGE_LENGTH)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        if isinstance(json_response, str):
            response = json.loads(json_response)
            if isinstance(response, dict):
                return response
            raise ValueError
        raise ValueError
    raise ValueError


def send_message(sock, message):
    # Утилита кодирования и отправки сообщения
    # принимает словарь и отправляет его
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)
