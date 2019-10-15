# -*- coding: utf-8 -*-
from datetime import datetime
import time
import RPi.GPIO as GPIO
import logging
from packs import sensorReader
from packs import sensorSender
from socket import socket, AF_INET, SOCK_DGRAM


class HumanSensor(sensorReader.SensorReader, sensorSender.SensorSender):
    def __init__(self, gpioPin, address, port, logger, log=None, name=None, coolTime=15):
        super(HumanSensor, self).__init__(gpioPin, logger, log, name)
        super(sensorReader.SensorReader, self).__init__(address, port, logger, log)
        self.STREAM_HANDLER.setFormatter(logging.Formatter('%(asctime)s,%(levelname)s'))
        self.LOGGER.addHandler(self.STREAM_HANDLER)
        self.LOGGER.addHandler(logging.FileHandler(log if log is not None else "sensor.log"))
        self.COOL_TIME = coolTime

    # 人感センサーの計測を開始するメソッド
    def start(self, executor):
        return executor.submit(fn=self.work)

    # 人感センサーの計測を行う
    def work(self):
        print(self.LOG_FILE)
        self.IS_WORKING = True
        try:
            while self.IS_WORKING:
                if GPIO.input(self.GPIO_PIN) == GPIO.HIGH:
                    # ログに計測した日時を出力する
                    self.LOGGER.info("")
                    # UDP
                    self.sendUDP("1")
                    time.sleep(self.COOL_TIME)

        finally:
            self.LOGGER.error("")
            self.IS_WORKING = False
            print("finished")

    # 人感センサーの値をUDP送信するためのクラス
    def send(self):
        pass

    def sendUDP(self, msg):
        s = socket(AF_INET, SOCK_DGRAM)
        while True:
            s.sendto(msg.encode(), (self.ADDRESS, self.PORT))

        s.close()
