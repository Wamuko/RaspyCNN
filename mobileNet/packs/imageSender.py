# -*- coding: utf-8 -*-
from packs import sensorBase
import picamera
import picamera.array
import numpy as np
import cv2
from mvnc import mvncapi as mvnc
from os import system
import io, time
import os.path
from datetime import datetime
from os.path import isfile, join
import re
from time import time

import socket

'''
PiCameraから画像を取得して、指定されたサーバに送信するクラス
@param SERVER_IP string 送りつけサーバIP
@param SERVER_PORT int サーバのポート指定
@param INTERVAL int 撮影を行うインターバル
@param SLEEP_TIME int(秒) この秒数だけ画像を送信を行う 

'''


class ImageSender(sensorBase.SensorBase):
    SERVER_IP = None
    SERVER_PORT = 50000
    INTERVAL = 2.5
    SLEEP_TIME = 15
    IS_WORKING = False

    def __init__(self, ip, port=None, interval=None):
        self.SERVER_IP = ip
        self.INTERVAL = interval if interval is not None else self.INTERVAL
        self.SERVER_PORT = port if port is not None else self.SERVER_PORT

    def start(self):
        # もし既にこの関数が動いていたら複数回は呼び出されないようにする
        if self.IS_WORKING:
            return
        else:
            self.IS_WORKING = True

        try:
            with picamera.PiCamera(resolution=(304, 304)) as camera:
                with picamera.array.PiRGBArray(camera) as stream:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
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
                            s.connect((self.SERVER_IP, self.SERVER_PORT))
                            # s.connect(('172.16.202.1', 50000))
                            # サーバにメッセージを送る
                            s.sendall(stream.array)
                            #
                            print('data sent')

                            if cv2.waitKey(1) & 0xFF == ord('q'):
                                break
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
