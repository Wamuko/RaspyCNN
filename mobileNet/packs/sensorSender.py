# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
from logging import getLogger, StreamHandler, Formatter, INFO
from abc import ABCMeta, abstractmethod


'''
@Abstract class
GPIOセンサーから値を受け取るクラス
継承専用
@GPIO_PIN param int GPIO PIN番号
@LOG param string ログを保存するファイル名
@NAME param string 
'''


class SensorSender(metaclass=ABCMeta):
    ADDRESS = None
    PORT = None
    LOGGER = None
    IS_WORKING = False
    STREAM_HANDLER = None

    def __init__(self, address, port, logger, log=None):
        self.ADDRESS = address
        self.PORT = port
        self.LOGGER = logger
        self.LOG_FILE = log if log is not None else "sensor.log"
        # ロガーの設定
        self.LOGGER.setLevel(INFO)
        self.STREAM_HANDLER = StreamHandler()
        self.STREAM_HANDLER.setLevel(INFO)

    @abstractmethod
    def send(self, executor):
        pass

    def stop(self):
        self.IS_WORKING = False

