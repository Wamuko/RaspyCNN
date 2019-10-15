# -*- coding: utf-8 -*-
from datetime import datetime
import time
import RPi.GPIO as GPIO
import logging
from packs import sensorReader
from packs import sensorSender
from socket import socket, AF_INET, SOCK_DGRAM
from logging import FileHandler, INFO, Formatter


class HumanSensor(sensorReader.SensorReader, sensorSender.SensorSender):
    def __init__(self, gpioPin, address, port, logger, log=None, name=None, coolTime=15):
        super(HumanSensor, self).__init__(gpioPin, logger, log, name)
        super(sensorReader.SensorReader, self).__init__(address, port, logger, log)

        self.COOL_TIME = coolTime
        filehandler = FileHandler(self.LOG_FILE)
        filehandler.setLevel(INFO)
        filehandler.setFormatter(Formatter('%(asctime)s %(levelname)s %(message)s'))
        self.LOGGER.addHandler(filehandler)


    # 人感センサーの計測を開始するメソッド
    def start(self, executor):
        return executor.submit(fn=self.work)

    # 人感センサーの計測を行う
    def work(self):
        self.IS_WORKING = True
        try:
            while self.IS_WORKING:
                if GPIO.input(self.GPIO_PIN) == GPIO.HIGH:
                    # ログに計測した日時を出力する
                    self.LOGGER.info(self.NAME)
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
        s.sendto(msg.encode(), (self.ADDRESS, self.PORT))
        s.close()
        print("send sensor data")
