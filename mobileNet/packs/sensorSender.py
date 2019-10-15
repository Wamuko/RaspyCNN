# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
from logging import getLogger, FileHandler, Formatter, INFO
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
    S_LOGGER = None
    S_IS_WORKING = False

    def __init__(self, address, port, logger, log=None):
        self.ADDRESS = address
        self.PORT = port
        self.S_LOGGER = logger
        self.S_LOG_FILE = log if log is not None else "sensor.log"
        # ロガーの設定
        self.S_LOGGER.setLevel(INFO)


    @abstractmethod
    def send(self):
        pass

    def stop(self):
        self.S_IS_WORKING = False

