import RPi.GPIO as gp
import time
from abc import ABCMeta, abstractmethod

'''
@Abstract class
センサーから値を受け取り
'''


class SensorReader(metaclass=ABCMeta):
    pass
