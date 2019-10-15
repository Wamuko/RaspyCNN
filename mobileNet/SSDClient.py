# -*- coding: utf-8 -*-
import sys, os
from socket import socket, AF_INET, SOCK_DGRAM

if sys.version_info.major < 3 or sys.version_info.minor < 4:
    print("Please using python3.4 or greater!")
    exit(1)

from packs import humanSensor as hs
from packs import imageHandler as isend
from packs import sensorThreader as st
from logging import getLogger

from packs import test as ts


def main():
    # ログ作成用初期処理
    logger = getLogger("sensors")
    logDir = os.path.join(os.getcwd(), "log")
    if not os.path.exists(logDir):
        os.mkdir(logDir)

    # センサーの定義
    sensors = [
        hs.HumanSensor(18, '10.10.2.126', 55550, logger, os.path.join(logDir, "humanSensor.log"), "HumanSensor-1"),
        hs.HumanSensor(12, '10.10.2.126', 55550, logger, os.path.join(logDir, "humanSensor.log"), "HumanSensor-2"),
        isend.ImageHandler('10.10.2.126', 50000, '10.10.2.126', 55550, logger, os.path.join(logDir, "imageSender.log")),
        ts.Test(50000),
    ]

    # スレッド処理するスレッドクラスの初期化
    threader = st.SensorThreader(sensors, 4)
    threader.start()


if __name__ == "__main__":
    main()
