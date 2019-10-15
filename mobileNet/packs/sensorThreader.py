# -*- coding: utf-8 -*-
from concurrent import futures

'''
複数センサを定義してそれらからの情報取得を並列化するクラス
必要な引数としては、最大ワーカー数、センサー(設定)リストを与える
@param workers 実際に並列で動作するタスクの最大数
@param sensors
'''


class SensorThreader:
    def __init__(self, sensors, workers=6):
        self.workers = workers
        self.sensors = sensors
        self.futuresList = []

    def start(self):
        with futures.ThreadPoolExecutor(max_workers=self.workers) as executor:
            for sensor in self.sensors:
                # future = executor.submit(fn=sensor.start())
                future = sensor.start(executor)
                self.futuresList.append(future)
            _ = futures.as_completed(self.sensors)
