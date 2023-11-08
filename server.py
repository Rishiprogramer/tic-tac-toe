import socket
import threading
import time

ip = socket.gethostbyname(socket.gethostname())
accept_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
accept_server.bind((ip, 8120))
accept_server.listen()
print(f"The server is listining on {ip}")
players_on_server = []
connected_pairs = []
nick_name = []


def x_or_o(p1, a1, p2, a2):
    a1.send('x'.encode('utf-16'))
    a1.send(p2.encode('utf-16'))
    a2.send('o'.encode('utf-16'))
    a2.send(p1.encode('utf-16'))
    draw_fig1 = False
    row2 = ""
    col2 = ""
    row1 = ""
    col1 = ""
    while True:
        a1.send('1'.encode('utf-16'))
        if draw_fig1:
            a1.send(row2.encode())
            time.sleep(0.2)
            a1.send(col2.encode())

        row1 = a1.recv(1024).decode()
        time.sleep(0.2)
        col1 = a1.recv(1024).decode()
        a1.send('ok'.encode('utf-16'))
        print(type(row1), col1)

        a2.send('2'.encode('utf-16'))
        a2.send(row1.encode())
        print('row  sending')
        time.sleep(0.2)
        a2.send(col1.encode())
        print('col sended')
        row2 = a2.recv(1024).decode()
        time.sleep(0.2)
        col2 = a2.recv(1024).decode()
        a2.send('ok'.encode('utf-16'))
        draw_fig1 = True



def connect_pair():
    while True:
        if len(players_on_server) > 1:
            details_of_p1 = players_on_server[0]
            details_of_p2 = players_on_server[1]
            name1 = details_of_p1[0]
            ip1 = details_of_p1[1]
            name2 = details_of_p2[0]
            ip2 = details_of_p2[1]
            players_on_server.remove(details_of_p2)
            players_on_server.remove(details_of_p1)
            time.sleep(1)
            threading.Thread(target=x_or_o, args=(name1, ip1, name2, ip2)).start()


def accept():
    while True:
        client, address = accept_server.accept()
        nickname = client.recv(1024).decode('utf-16')
        print(f'{nickname} joined the server')
        if nickname in nick_name:
            nicknam = str(len(nick_name) + 1)
            nickname = nickname+nicknam
            nick_name.append(nickname)
        print("updated", nickname)
        nick_name.append(nickname)
        players_on_server.append((nickname, client))


threading.Thread(target=accept).start()
threading.Thread(target=connect_pair).start()
