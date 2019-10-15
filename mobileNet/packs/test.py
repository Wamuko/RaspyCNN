from socket import socket, AF_INET, SOCK_DGRAM

class Test:
    def __init__(self):
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind(('10.10.2.126', 5000))

    def start(self, executor):
        return executor.submit(fn=self.test)

    def test(self):
        # デバックのために地震の5000番ポートになんか飛んで来たらプリントする
        print("Waiting images")

        while True:
            msg, address = self.sock.recvfrom(8192)
            print("Got Images!!\n")

        s.close()