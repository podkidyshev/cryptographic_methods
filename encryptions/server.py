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
    name = sock.recv(BUFSIZ).decode("utf8")

    if name == '{quit}':
        # Если вдруг кто-то не захотел болтать
        print('{} отсоединился'.format(address))
        sock.send(bytes("{quit}", "utf8"))
        sock.close()
        return

    client = Client(sock, address, name)
    # Прибывший
    welcome = 'Бобро пожаловать, {}! Если хотите выйти – введите {{quit}}.'.format(client.name)
    client.sock.send(bytes(welcome, "utf8"))
    # Скажем остальным
    msg = "{} присоединился к чату!".format(client.name)
    broadcast(bytes(msg, "utf8"))

    while True:
        msg = client.sock.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, "{}: ".format(client.name))
        else:
            # разрываем соединение с этим клиентом
            name = client.name
            address = client.address
            client.sock.send(bytes("{quit}", "utf8"))
            client.delete()
            # Оповещение
            broadcast(bytes("{} покинул чат.".format(name), "utf8"))
            print('{} отсоединился'.format(address))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Рассылаем сообщение всем клиентам"""
    for sock in Client.BASE:
        sock.send(bytes(prefix, "utf8") + msg)


class Client:
    BASE = {}

    def __init__(self, sock, address, name):
        self.sock = sock
        self.address = address
        self.name = name
        self.pwd = random.getrandbits(128).to_bytes(aes.KEY_SIZE_BYTES, byteorder='big')
        # запоминаем челика
        Client.BASE[self.sock] = self

    def delete(self):
        del Client.BASE[self.sock]
        self.sock.close()

        
HOST = ''
PORT = 33001
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
