from socket import socket, AF_INET, SOCK_STREAM

class Test:
    def __init__(self, port):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind(('10.10.2.126', port))

    def start(self, executor):
        return executor.submit(fn=self.test)

    def test(self):
        # デバックのために地震の50000番ポートになんか飛んで来たらプリントする
        print("Waiting images")
        self.sock.listen(1)

        while True:
            msg, address = self.sock.recvfrom(8192)
            print("Got Images!!\n")

        self.sock.close()