# -*- coding: utf-8 -*-
from datetime import datetime
import time
import RPi.GPIO as GPIO
import logging
from packs import sensorReader
import os

'''
人勧センサーの値を読み取るためのクラス
'''


class HumanSensorReader(sensorReader.SensorReader):
    def __init__(self, gpioPin,logger, imageSender, log=None, name=None):
        super().__init__(gpioPin, logger, log, name)
        self.imageSender = imageSender
        # Loggerの振る舞いを定義
        self.STREAM_HANDLER.setFormatter(logging.Formatter('%(asctime)s,%(levelname)s'))
        self.LOGGER.addHandler(self.STREAM_HANDLER)
        self.LOGGER.addHandler(logging.FileHandler(log if log is not None else "sensor.log"))

    # センサーの読み取りをスタートする
    def start(self):
        self.IS_WORKING = True
        try:
            while self.IS_WORKING:
                if GPIO.input(self.GPIO_PIN) == GPIO.HIGH:
                    self.LOGGER.info("")
                    # 電灯を点火
                    os.system("./lib/rgb_led.pl 0000FF")
                    # ついでにスイッチを動かす
                    os.system("./lib/switch_bot")
                    # 画像の送信を開始
                    # ↓の処理が終わるまで待ってくれるのかわからない
                    self.imageSender.start()
                    # 消灯
                    os.system("./lib/rgb_led off")

        finally:
            self.LOGGER.error("stoped")
            self.IS_WORKING = False

