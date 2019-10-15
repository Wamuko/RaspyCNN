from socket import socket, AF_INET, SOCK_DGRAM

class Test:
    def start(self, executor):
        return executor.submit(fn=test)

    def test(self):
        # デバックのために地震の5000番ポートになんか飛んで来たらプリントする
        s = socket(AF_INET, SOCK_DGRAM)
        s.bind(('', 5000))

        while True:
            msg, address = s.recvfrom(8192)
            print("画像が送られてきたよ")

        s.close()