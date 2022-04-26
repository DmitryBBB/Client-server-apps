from select import select
from socket import socket, AF_INET, SOCK_STREAM


def read_requests(read_clients, all_clients):
    # Чтение запросов из списка клиентов
    responses = {}
    for sock in read_clients:
        try:
            data = sock.recv(1024).decode('utf-8')
            responses[sock] = data
        except Exception as e:
            print(e)
            print(f'Клиент {sock.fileno()} {sock.getpeername()} отключился')
            sock.close()
            all_clients.remove(sock)

    return responses


def write_responses(requests, clients_write, all_clients):
    # Эхо ответ сервера клиентам, от которых были запросы

    for sock in clients_write:
        if sock in requests:
            try:
                if requests[sock] == '':
                    raise Exception
                resp = requests[sock].upper()
                print(resp)
                sock.send(resp.encode('utf-8'))
            except Exception as e:
                print(e)
                # sock.fileno() - вернуть дескриптор файла сокета
                # sock.getpeername() - получить IP адрес и номер порта клиента
                print(f'Клиент {sock.fileno()} {sock.getpeername()} отключился')
                all_clients.remove(sock)
                sock.close()


def mainloop():
    # Основной цикл обработки запросов клиентов
    address = ('', 10000)
    all_clients = []

    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.bind(address)
        sock.listen(5)
        sock.settimeout(1)
        while True:
            try:
                conn, addr = sock.accept()
            except OSError as er:
                pass
            else:
                print(f'Получен запрос на соединение от {str(addr)}')
                all_clients.append(conn)
            finally:
                wait = 0
                clients_read = []
                clients_write = []
                try:
                    clients_read, clients_write, errors = select(all_clients, all_clients, [], wait)

                except Exception as e:
                    print(e)
                    pass
                requests = read_requests(clients_read, all_clients)
                print(requests)
                if requests:
                    write_responses(requests, clients_write, all_clients)


if __name__ == '__main__':
    mainloop()
