import socket
import threading
import time


class ChatServer:
    def __init__(self):
        self.col = None
        self.row = None
        self.two_p1 = None
        self.idxs = None
        self.idx2s = None
        self.idx2 = None
        self.idx = None
        self.ip = socket.gethostbyname(socket.gethostname())
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.ip, 5240))
        self.server.listen()
        self.available = []
        self.clients = []
        self.matches = []
        self.matched_pairs = set()
        print(self.ip)

    def matches_going_on(self, pair):
        player1s = pair[0]
        player2s = pair[1]
        self.idxs = self.available.index(player1s)
        self.idx2s = self.available.index(player2s)
        client1s = self.clients[self.idxs]
        client2s = self.clients[self.idx2s]
        self.two_p1 = False
        self.available.remove(self.idxs)
        self.available.remove(self.idx2s)
        while True:
            try:
                #send the player one that it is your turn
                client1s.send('1'.encode('utf-16'))
                if self.two_p1:
                    print("sending")
                    time.sleep(0.5)
                    client1s.send(self.row.encode('utf-16'))
                    time.sleep(0.5)
                    client1s.send(self.col.encode('utf-16'))
                    time.sleep(0.5)
                    print(self.row, self.col)
            #takes the row and col from player 1
                self.row = client1s.recv(1024).decode()
                time.sleep(0.5)
                self.col = client1s.recv(1024).decode()
                time.sleep(0.5)
                client1s.send('ok received'.encode('utf-16'))
            #prints the type
                print(type(self.row), type(self.col))

            #send to client two that it is your turn
                client2s.send('2'.encode('utf-16'))
                time.sleep(0.5)

            #sends the row and col where the player one has marked
                client2s.send(str(self.row).encode('utf-16'))
                time.sleep(0.5)
                client2s.send(str(self.col).encode('utf-16'))
                time.sleep(0.5)
            #recives the row and col from player two
                self.row = client2s.recv(1024).decode()
                time.sleep(0.5)
                self.col = client2s.recv(1024).decode()
                time.sleep(0.5)
                client2s.send('ok received'.encode('utf-16'))

                self.two_p1 = True
                print(self.row, self.col)
            except Exception as e:
                client1s.close()
                client2s.close()
                self.clients.remove(self.idxs)
                self.clients.remove(self.idx2s)


    def decide_X_OR_O(self):
        if len(self.matches) > 0:
            for pair in self.matches:
                player1 = pair[0]
                player2 = pair[1]
                self.idx = self.available.index(player1)
                self.idx2 = self.available.index(player2)
                client1 = self.clients[self.idx]
                client2 = self.clients[self.idx2]
                client1.send('X'.encode('utf-16'))
                client2.send('0'.encode('utf-16'))
                threading.Thread(target=self.matches_going_on, args=(pair,)).start()

    def connect(self, client, nickname):
        found_match = False

        for avai in self.available:
            if avai != nickname:
                pair = (avai, nickname)
                if pair not in self.matched_pairs:
                    self.matched_pairs.add(pair)
                    client.send(avai.encode('utf-16'))
                    clientm = self.clients[self.clients.index(client) - 1]
                    clientm.send(nickname.encode('utf-16'))
                    self.matches.append((avai, nickname))
                    found_match = True
                    break

        if found_match:
            threading.Thread(target=self.decide_X_OR_O).start()
            # print(self.matches)

    def receive_clients(self):
        while True:
            client, address = self.server.accept()
            print("Connected with", address)
            try:
                nickname = client.recv(1048576).decode('UTF-16')

                self.available.append(nickname)
                self.clients.append(client)

                print("Nickname of the client is", nickname)

                thread = threading.Thread(target=self.connect, args=(client, nickname))
                thread.start()
            except Exception as e:
                client.close()

    def run(self):
        receive_thread = threading.Thread(target=self.receive_clients)
        receive_thread.start()


if __name__ == '__main__':
    chat_server = ChatServer()
    chat_server.run()
