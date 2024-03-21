from random import choice
import socket
import os
from threading import Thread
from colorama import Fore, init

init()
colors = [Fore.RED, Fore.YELLOW, Fore.GREEN,
          Fore.BLUE, Fore.CYAN, Fore.MAGENTA,
          Fore.WHITE, Fore.BLACK]
client_color = choice(colors)

if not os.path.exists('ip.txt'):
    SERVER_HOST = input('Введите ip сервера: ')
    SERVER_PORT = input('Введите порт сервера: ')
    NAME = input("Как тебя зовут? ")
    with open('ip.txt', 'w', encoding='utf8') as f:
        f.write(f'{SERVER_HOST}\n{SERVER_PORT}\n{NAME}')
else:
    with open('ip.txt', encoding='utf8') as f:
        SERVER_HOST, SERVER_PORT, NAME = f.read().split('\n')

SEPARATOR_TOKEN = "<SEP>"  # separates the client NAME & message
send_to = ''

s = socket.socket()
print(f"[*] Подключение к {SERVER_HOST}:{SERVER_PORT}...")
s.connect((SERVER_HOST, int(SERVER_PORT)))
print("[+] Подключено")

s.send(NAME.encode())  # send the NAME to server


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
        command = input('Настройки:\n1 - выбрать цвет\n2 - кому отправлять по умолчанию\n3 - выбрать ip и порт сервера\n4 - сменить имя\nВвод - выход')
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
        elif command == '3':
            SERVER_HOST = input('Введите новый ip сервера: ')
            SERVER_PORT = input('Введите новый порт сервера: ')
            with open('ip.txt', 'w', encoding='utf8') as f:
                f.write(f'{SERVER_HOST}\n{SERVER_PORT}\n{NAME}')
        elif command == '4':
            NAME = input("Как теперь тебя зовут? ")
            with open('ip.txt', 'w', encoding='utf8') as f:
                f.write(f'{SERVER_HOST}\n{SERVER_PORT}\n{NAME}')

    else:
        if '@' in to_send:
            to_send = f'{client_color}{NAME}{Fore.RESET}{SEPARATOR_TOKEN}{to_send}'
        else:
            to_send = f'{client_color}{NAME}{Fore.RESET}{SEPARATOR_TOKEN}{send_to}{to_send}'


s.close()
