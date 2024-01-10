import random
import socket
from threading import Thread
from colorama import Fore, init

init()
colors = [Fore.RED, Fore.YELLOW, Fore.GREEN,
          Fore.BLUE, Fore.CYAN, Fore.MAGENTA,
          Fore.WHITE, Fore.BLACK]
client_color = random.choice(colors)

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 50025
SEPARATOR_TOKEN = "<SEP>"  # separates the client name & message
send_to = ''

name = input("Как тебя зовут? ")

s = socket.socket()
print(f"[*] Подключение к {SERVER_HOST}:{SERVER_PORT}...")
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Подключено")

s.send(name.encode())  # send the name to server


def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        print("\n" + message)


# listen for messages to this client & print them
t = Thread(target=listen_for_messages)
t.daemon = True
t.start()

while True:
    to_send = input()

    if to_send == '#exit':
        break

    elif to_send == '#settings':
        command = input('Настройки:\n1 - выбрать цвет\n2 - кому отправлять по умолчанию\nВвод - выход')
        if command == '1':
            num = 0
            for color in colors:
                print(num, f'{color}Текст{Fore.RESET}')
                num += 1
            new_color = input('Введите номер цвета, \'\' - отмена: ')
            if new_color:
                client_color = colors[int(new_color)]
        elif command == '2':
            s.send('#list'.encode())
            send_to = input('Кому отправлять?') + '@'

    else:
        if '@' in to_send:
            to_send = f'{client_color}{name}{Fore.RESET}{SEPARATOR_TOKEN}{to_send}'
        else:
            to_send = f'{client_color}{name}{Fore.RESET}{SEPARATOR_TOKEN}{send_to}{to_send}'
        s.send(to_send.encode())

s.close()
