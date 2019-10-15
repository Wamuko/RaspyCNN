from socket import socket, AF_INET, SOCK_DGRAM

class Test:
    def start(self, executor):
        return executor.submit(fn=self.test)

    def test(self):
        # デバックのために地震の5000番ポートになんか飛んで来たらプリントする
        s = socket(AF_INET, SOCK_DGRAM)
        s.bind(('10.10.2.126', 5000))
        print("Waiting images")

        while True:
            msg, address = s.recvfrom(8192)
            print("Got Images!!\n")

        s.close()