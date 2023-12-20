import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init

# init colors, set the available colors and choose a random color for the client
init()
colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX,
          Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX,
          Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX,
          Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
          ]
client_color = random.choice(colors)


# if the server is not on this machine, put the private (network) IP address (e.g. 192.168.1.2)
SERVER_HOST = "127.0.0.1"  # server's IP address
SERVER_PORT = 50025  # server's port
separator_token = "<SEP>"  # we will use this to separate the client name & message

name = input("Enter your name: ")  # ask for a name

# initialize TCP socket and connect to the server
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")

s.send(name.encode())  # send the name to server


def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        print("\n" + message)


# make a thread that listens for messages to this client & print them
t = Thread(target=listen_for_messages)
# make the thread daemon, so it ends whenever the main thread ends
t.daemon = True
# start the thread
t.start()

while True:
    # input message we want to send to the server
    to_send = input()

    # exit the program
    if to_send == '/exit':
        break

    # add name and the color of the sender
    to_send = f"{client_color}{name}{Fore.RESET}{separator_token}{to_send}"
    # send the message
    s.send(to_send.encode())

# close the socket and exit
s.close()
