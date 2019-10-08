# -*- coding: utf-8 -*-
from datetime import datetime
import time
import RPi.GPIO as GPIO
import logging
from packs import sensorReader


class HumanSensorReader(sensorReader.SensorReader):
    def __init__(self, gpioPin,logger, log=None, name=None):
        super().__init__(gpioPin, logger, log, name)
        self.STREAM_HANDLER.setFormatter(logging.Formatter('%(asctime)s,%(levelname)s'))
        self.LOGGER.addHandler(self.STREAM_HANDLER)
        self.LOGGER.addHandler(logging.FileHandler(log if log is not None else "sensor.log"))

    def start(self):
        self.IS_WORKING = True
        try:
            while self.IS_WORKING:
                if GPIO.input(self.GPIO_PIN) == GPIO.HIGH:
                    self.LOGGER.info()
        finally:
            self.LOGGER.err()
