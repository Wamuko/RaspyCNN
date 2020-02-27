# -*- coding: utf-8 -*-
import errno
import os.path
import socket
from PIL import Image
import sys
import time
import cv2

import numpy as np


# センサーと同じように非同期処理で走らせるので、superクラスをimplementする形の方がよかったかも
class ImgSaver:
    def __init__(self, ip_from, port_from):
        self.IS_WORKING = False
        self.ip_from = ip_from
        self.port_from = port_from

        # 画像保存用ディレクトリの作成
        segmented_images_dir = "saved_images"
        self.segmented_images_path = os.path.join(os.getcwd(), segmented_images_dir)
        if not os.path.exists(self.segmented_images_path):
            os.makedirs(self.segmented_images_path)

    # TCPで特定サイズの画像を1枚受け取るためのメソッド
    def __myrcv(self, conn, length):
        chunks = []
        bytes_recd = 0
        while bytes_recd < length:
            try:
                chunk = conn.recv(min(length - bytes_recd, length))
                if chunk == b'':
                    return False
                chunks.append(chunk)
                bytes_recd = bytes_recd + len(chunk)
            except socket.error as e:
                if e.errno == errno.ECONNRESET:
                    return False

        return b''.join(chunks)

    def work(self):
        if self.IS_WORKING:
            return
        else:
            self.IS_WORKING = True
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # IPアドレスとポートを指定
                s.bind((self.ip_from, self.port_from))
                # 1 接続
                s.listen(1)
                # connection するまで待つ
                while True:
                    # 誰かがアクセスしてきたら、コネクションとアドレスを入れる
                    print("接続待機中")
                    conn, addr = s.accept()
                    with conn:
                        frames = 0
                        # 指定された秒数だけ受信・解析を行う
                        while True:
                            print("データ待機中")
                            t1 = time.perf_counter()
                            # データを受け取る
                            data = self.__myrcv(conn, 304 * 304 * 3)
                            if not data:
                                break

                            # Convert images to numpy array
                            encoded = np.frombuffer(data, np.uint8)
                            color_image = np.reshape(encoded, (304, 304, 3))
                            # ディレクトリにJPGイメージを保存する
                            cv2.imwrite(os.path.join(self.segmented_images_path, str(addr[0])) + '.jpg', color_image)
                            cv2.imshow(str(addr[0]), color_image)

        except:
            import traceback
            traceback.print_exc()

        finally:
            print("\n\nFinished\n\n")
            cv2.destroyAllWindows()
            sys.exit()


if __name__ == "__main__":
    # args: {1: 送信元のアドレス，2: 送信元のポート}
    cam = ImgSaver('0.0.0.0', int(sys.argv[1]))
    cam.work()
    cv2.destroyAllWindows()
