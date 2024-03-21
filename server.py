import pickle
import socket
from threading import Thread


def get_local_ip() -> str:
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip


SERVER_PORT = 50025
SERVER_HOST = get_local_ip()

SEPARATOR_TOKEN = "<SEP>"

client_sockets = dict()

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)

print(f"[*] Сервер работает на {SERVER_HOST}:{SERVER_PORT}")


def control_thread(c_sockets: dict) -> None:
    while True:
        command = input()
        if command == 'list':
            for i in c_sockets:
                print(i)

        elif 'del ' in command:
            del_clients = command.split()[1:]
            for i in del_clients:
                c_sockets[i].close()
                del c_sockets[i]

        elif 'send ' in command:
            text = command.split()[1:]
            for name, client in c_sockets.items():
                client.send(('SERVER: ' + ' '.join(text)).encode())


def listen_for_client(cs, client_name):
    while True:
        try:
            msg = cs.recv(1024).decode()
            print('Получено сообщение: ', msg)

        except Exception as e:
            print(f"[!] Ошибка: {e}")
            print(f"[!!] Клиент {client_name} отключен из-за ошибки")
            del client_sockets[client_name]
            return

        else:
            if not msg:
                del client_sockets[client_name]
                print(f"[!] Клиент {client_name} отключен")
                return

            msg = msg.replace(SEPARATOR_TOKEN, ": ")

            text_to_send = msg.split(': ')[-1]

            command = ''
            send_to_client = ''
            if '@' in text_to_send:
                send_to_client = text_to_send.split('@')[0]
                command = ''
            elif '#' in text_to_send:
                command = text_to_send

            if send_to_client:
                try:
                    client_sockets[send_to_client].send(
                        (msg.split(': ')[0] + ': ' + text_to_send.split('@')[1]).encode())
                except KeyError:
                    cs.send('Такого нет!!!'.encode())

            elif command:
                if command == '#list':
                    clients_to_send = ''
                    for sockets in client_sockets:
                        clients_to_send += f'- {sockets}\n'
                    cs.send(clients_to_send.encode())

            else:
                for sockets in client_sockets:
                    print(sockets)
                    client_sockets[sockets].send(msg.encode())


control_th = Thread(target=control_thread, args=(client_sockets,))
control_th.daemon = True
control_th.start()

while True:
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} подключился")

    client_name = client_socket.recv(1024).decode()
    client_sockets[client_name] = client_socket

    t = Thread(target=listen_for_client, args=(client_socket, client_name))
    t.daemon = True
    t.start()
