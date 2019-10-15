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
            conn, addr = self.sock.accept()
            with conn:
                while True:
                    data = conn.recv(300*300*3)
                    if not data:
                        continue
                    print("Got Images!!\n")

        self.sock.close()