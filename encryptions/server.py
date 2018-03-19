#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import random

from messages import *


def accept_incoming_connections():
    """Обрабатываем новые подключения"""
    while True:
        sock, address = SERVER.accept()
        print("{} присоединился.".format(address))
        sock.send(handle_send("День добрый! Введите имя и нажмите Enter!"))
        Thread(target=handle_client, args=(sock, address)).start()


def handle_client(sock, address):  # Takes client socket as argument.
    """Хэндлим клиента"""
    # Получим ник
    name = handle_receive(sock.recv(BUFSIZ))['msg']

    if name == '{quit}':
        # Если вдруг кто-то не захотел болтать
        print('{} отсоединился'.format(address))
        sock.send(handle_send("{quit}"))
        sock.close()
        return

    client = Client(sock, address, name)
    # Прибывший
    welcome = 'Бобро пожаловать, {}! Если хотите выйти – введите {{quit}}.'.format(client.name)
    client.sock.send(handle_send(welcome, pwd=client.pwd))
    # Скажем остальным
    msg = "{} присоединился к чату!".format(client.name)
    broadcast(msg)

    while True:
        msg = handle_receive(client.sock.recv(BUFSIZ), key_in=client.get_pwd())['msg']
        if msg != "{quit}":
            broadcast(msg, "{}: ".format(client.name))
        else:
            # разрываем соединение с этим клиентом
            name = client.name
            address = client.address
            client.sock.send(handle_send("{quit}"))
            client.delete()
            # Оповещение
            broadcast("{} покинул чат.".format(name))
            print('{} отсоединился'.format(address))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Рассылаем сообщение всем клиентам"""
    for sock in Client.BASE:
        sock.send(handle_send(prefix + msg, key_out=Client.BASE[sock].get_pwd()))


class Client:
    BASE = {}

    def __init__(self, sock, address, name):
        self.sock = sock
        self.address = address
        self.name = name
        self.pwd = random.getrandbits(128)  # .to_bytes(aes.KEY_SIZE_BYTES, byteorder='big')
        print('Для клиента {} сгенерирован ключ {}'.format(self.name, self.pwd))
        # запоминаем челика
        Client.BASE[self.sock] = self

    def get_pwd(self):
        return self.pwd.to_bytes(aes.KEY_SIZE_BYTES, byteorder='big')

    def delete(self):
        del Client.BASE[self.sock]
        self.sock.close()

        
HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Жду соединения...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
