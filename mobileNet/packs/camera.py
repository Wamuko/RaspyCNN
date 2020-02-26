# -*- coding: utf-8 -*-
from packs import sensorSender
import picamera
import picamera.array
import time
import subprocess
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM
from logging import FileHandler, INFO, Formatter
import sys

'''
PiCameraから画像を取得して、指定されたサーバに送信するクラス
@param SERVER_IP string 送りつけサーバIP
@param SERVER_PORT int サーバのポート指定
@param INTERVAL int 撮影を行うインターバル
@param SLEEP_TIME int(秒) この秒数だけ画像を送信を行う 

'''


class ImageHandler:
    INTERVAL = 2.5
    SLEEP_TIME = 8
    LISTENING_PORT = None
    ADDRESS = None
    PORT = None

    def __init__(self, address, port, interval=None, sleep=None):
        self.INTERVAL = interval if interval is not None else self.INTERVAL
        self.SLEEP_TIME = sleep if sleep is not None else self.SLEEP_TIME
        self.ADDRESS = address
        self.PORT = port

    # 画像を他の機器に送信するためのメソッド
    def send(self):
        try:
            with picamera.PiCamera(resolution=(304, 304)) as camera:
                with picamera.array.PiRGBArray(camera) as stream:
                    with socket(AF_INET, SOCK_STREAM) as s:
                        # サーバを指定
                        s.connect((self.ADDRESS, self.PORT))
                        # 処理を開始した時刻を取得
                        timeSta = time.perf_counter()
                        timeEnd = time.perf_counter()
                        while timeEnd - timeSta <= self.SLEEP_TIME:
                            # 写真を撮り始めた時間
                            timeImageSta = time.perf_counter()
                            interval = self.INTERVAL
                            # stream.arrayにRGBの順で映像データを格納
                            camera.capture(stream, 'bgr', use_video_port=True)

                            t1 = time.perf_counter()

                            # Wait for a coherent pair of frames: depth and color
                            if not stream:
                                continue

                            # Convert images to numpy arrays
                            # color_image = np.asanyarray(stream.array)

                            # s.connect(('172.16.202.1', 50000))
                            # サーバにメッセージを送る
                            s.sendall(stream.array.tostring())

                            stream.seek(0)
                            stream.truncate()
                            # インターバルの時間分スリープする
                            time.sleep(interval - (timeImageSta - time.perf_counter()))
                            timeEnd = time.perf_counter()
                        s.close()
        except Exception:
            import traceback

            traceback.print_exc()

        finally:
            self.S_IS_WORKING = False

    # 人感センサーの値を受け取るエージェントを起動
    def main(self):
        self.send()

if __name__ == "__main__":
    # args: {1: 送信先のアドレス，2: 送信先のポート}
    cam = ImageHandler(sys.argv[1], sys.argv[2])
    cam.main()
