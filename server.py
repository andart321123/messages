import socket
from threading import Thread

# server's IP address
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 50025  # port we want to use
separator_token = "<SEP>"  # we will use this to separate the client name & message

# initialize list/set of all connected client's sockets
client_sockets = dict()


s = socket.socket()  # create a TCP socket
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # make the port as reusable port
s.bind((SERVER_HOST, SERVER_PORT))  # bind the socket to the address we specified
s.listen(5)  # listen for upcoming connections

print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")


def control_thread(c_sockets: dict) -> None:
    while 1:
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


def listen_for_client(cs):
    """
    This function keep listening for a message from `cs` socket
    Whenever a message is received, broadcast it to all other connected clients
    """

    while True:
        try:
            # keep listening for a message from `cs` socket
            msg = cs.recv(1024).decode()
            print('message from client:', msg)

        except Exception as e:
            # client no longer connected
            print(f"[!] Error: {e}")
            break

        else:
            # if we received a message, replace the <SEP>
            # token with ": " for nice printing
            msg = msg.replace(separator_token, ": ")

            to_send = msg.split(': ')[-1]
            if len(to_send.split('@')) != 1:
                send_to = to_send.split('@')[0]
            else:
                send_to = ''

            # iterate over all connected sockets
            if send_to:
                try:
                    print(send_to)
                    client_sockets[send_to].send((msg.split(': ')[0] + ': ' + to_send.split('@')[1]).encode())
                except KeyError:
                    cs.send('Такого нет!!!'.encode())
            else:
                for sockets in client_sockets:
                    # отправляем сообщение всем клиентам
                    print(sockets)
                    client_sockets[sockets].send(msg.encode())


control_th = Thread(target=control_thread, args=(client_sockets,))
control_th.daemon = True
control_th.start()

while True:
    client_socket, client_address = s.accept()  # we keep listening for new connections all the time
    print(f"[+] {client_address} connected.")

    client_name = client_socket.recv(1024).decode()
    client_sockets[client_name] = client_socket  # add the new connected client to connected sockets

    # start a new thread that listens for each client's messages
    t = Thread(target=listen_for_client, args=(client_socket,))
    t.daemon = True  # make the thread daemon, so it ends whenever the main thread ends
    t.start()  # start the thread
