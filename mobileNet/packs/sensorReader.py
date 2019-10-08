# -*- coding: utf-8 -*-
import RPi.GPIO as gp
import time
from logging import getLogger, StreamHandler, Formatter, INFO
from packs import sensorBase

'''
@Abstract class
GPIOセンサーから値を受け取るクラス
継承専用
@GPIO_PIN param int GPIO PIN番号
@LOG param string ログを保存するファイル名
@NAME param string 
'''


class SensorReader(sensorBase.SensorBase):
    GPIO_PIN = None
    LOGGER = None
    NAME = None
    IS_WORKING = False
    STREAM_HANDLER = None

    def __init__(self, gpioPin, logger, log=None, name=None):
        self.GPIO_PIN = int(gpioPin)
        self.LOGGER = logger
        self.LOG_FILE = log
        self.NAME = name if name is not None else "Sensor"
        # GPIOの設定
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIO_PIN, GPIO.IN)
        # ロガーの設定
        self.LOGGER.setLevel(INFO)
        self.STREAM_HANDLER = StreamHandler()
        self.STREAM_HANDLER.setLevel(INFO)

    def stop(self):
        self.IS_WORKING = False

