from socket import socket, AF_INET, SOCK_STREAM

class Test:
    def __init__(self, port):
        self.PORT = port

    def start(self, executor):
        return executor.submit(fn=self.test)

    def test(self):
        # デバックのために地震の50000番ポートになんか飛んで来たらプリントする
        print("Waiting images")
        with socket(AF_INET, SOCK_STREAM) as s:
            s.listen(1)
            s.bind(('10.10.2.126', self.PORT))
            while True:
                conn, addr = s.accept()
                with conn:
                    while True:
                        data = conn.recv(300*300*3)
                        if not data:
                            continue
                    print("Got Image!!\n")
