# -*- coding: utf-8 -*-
from packs import sensorSender
import picamera
import picamera.array
import time
import subprocess
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM
from logging import FileHandler, INFO, Formatter


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
    LISTENING_PORT = None

    def __init__(self, address, port, listeningAddress, listeningPort, logger, log, interval=None, sleep=None, led_mac=None, led_color=None):
        super().__init__(address, port, logger, log)
        self.INTERVAL = interval if interval is not None else self.INTERVAL
        self.SLEEP_TIME = sleep if sleep is not None else self.SLEEP_TIME
        self.LISTENING_ADDRESS = listeningAddress
        self.LISTENING_PORT = listeningPort
        self.LED_MAC = led_mac
        self.LED_COLOR = led_color
        # ソケット定義
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind((self.LISTENING_ADDRESS, self.LISTENING_PORT))
        # loggerの初期化
        filehandler = FileHandler(self.S_LOG_FILE)
        filehandler.setLevel(INFO)
        filehandler.setFormatter(Formatter('%(asctime)s %(levelname)s %(message)s'))
        self.S_LOGGER.addHandler(filehandler)

    # 画像を他の機器に送信するためのメソッド
    def send(self):
        # もし既にこの関数が動いていたら複数回は呼び出されないようにする
        if self.S_IS_WORKING:
            print("already working")
            return
        else:
            self.S_IS_WORKING = True

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
                            self.S_LOGGER.info("got picture!")

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

    # LED電球を操作する、arg: "on", "off", "nnnnnn" (nは16進数)
    def led_operate(self, arg):
        if arg == "on" and self.LED_COLOR is not None:
            result = subprocess.check_output(["perl", "./lib/rgb_led.pl", self.LED_COLOR, self.LED_MAC], stdin=subprocess.PIPE)
        else:
            result = subprocess.check_output(["perl", "./lib/rgb_led.pl", arg, self.LED_MAC], stdin=subprocess.PIPE)
        return result

    # 人感センサーの値を受け取って、画像を送信するエージェントを起動する
    def start(self, executor):
        return executor.submit(fn=self.listening)

    # 人感センサーの値を受け取るエージェントを起動
    def listening(self):
        print("Waiting sensor data")
        print("address: {}, port: {}".format(self.LISTENING_ADDRESS, self.LISTENING_PORT))
        _ = self.led_operate("off")
        _ = self.led_operate("off")

        while True:
            msg, address = self.sock.recvfrom(32)
            if msg is not None and not self.S_IS_WORKING:
                _ = self.led_operate("on")
                _ = self.led_operate("on")
                self.send()
                _ = self.led_operate("off")
                _ = self.led_operate("off")

        self.sock.close()
