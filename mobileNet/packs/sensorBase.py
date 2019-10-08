# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

'''
全ての接続機器のベースとなる基底クラス
'''


class SensorBase(metaclass=ABCMeta):
    @abstractmethod
    def start(self):
        pass
