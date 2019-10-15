# -*- coding: utf-8 -*-
from packs import sensorSender
import picamera
import picamera.array
import time
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM

'''
PiCameraから画像を取得して、指定されたサーバに送信するクラス
@param SERVER_IP string 送りつけサーバIP
@param SERVER_PORT int サーバのポート指定
@param INTERVAL int 撮影を行うインターバル
@param SLEEP_TIME int(秒) この秒数だけ画像を送信を行う 

'''


class ImageHandler(sensorSender.SensorSender):
    INTERVAL = 2.5
    SLEEP_TIME = 11
    IS_WORKING = False
    LISTENING_PORT = None

    def __init__(self, address, port, listeningAddress, listeningPort, logger, log, interval=None, sleep=None):
        super().__init__(address, port, logger, log)
        self.INTERVAL = interval if interval is not None else self.INTERVAL
        self.SLEEP_TIME = sleep if sleep is not None else self.SLEEP_TIME
        self.LISTENING_ADDRESS = listeningAddress
        self.LISTENING_PORT = listeningPort
        # ソケット定義
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind((self.LISTENING_ADDRESS, self.LISTENING_PORT))

    # 画像を他の機器に送信するためのメソッド
    def send(self):
        # もし既にこの関数が動いていたら複数回は呼び出されないようにする
        if self.IS_WORKING:
            return
        else:
            self.IS_WORKING = True

        try:
            with picamera.PiCamera(resolution=(304, 304)) as camera:
                with picamera.array.PiRGBArray(camera) as stream:
                    with socket(AF_INET, SOCK_STREAM) as s:
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

                            # サーバを指定
                            s.connect((self.ADDRESS, self.PORT))
                            # s.connect(('172.16.202.1', 50000))
                            # サーバにメッセージを送る
                            s.sendall(stream.array)
                            #
                            self.LOGGER("image sent")

                            stream.seek(0)
                            stream.truncate()
                            # インターバルの時間分スリープする
                            time.sleep(interval - (timeImageSta - time.perf_counter()))
                            timeEnd = time.perf_counter()
        except Exception:
            import traceback

            traceback.print_exc()

        finally:
            self.IS_WORKING = False

    # 人感センサーの値を受け取って、画像を送信するエージェントを起動する
    def start(self, executor):
        return executor.submit(fn=self.listening)

    # 人感センサーの値を受け取るエージェントを起動
    def listening(self):
        print("Waiting sensor data")
        print("address: {}, port: {}".format(self.LISTENING_ADDRESS, self.LISTENING_PORT))

        while True:
            msg, address = self.sock.recvfrom(32)
            if msg is not None:
                self.send()
                print("send images")

        self.sock.close()
