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


def main():
    # ログ作成用初期処理
    logDir = os.path.join(os.getcwd(), "log")
    if not os.path.exists(logDir):
        os.mkdir(logDir)

    # センサーの定義
    sensors = [
        hs.HumanSensor(18, '10.10.2.126', 55550, getLogger("1"), os.path.join(logDir, "humanSensor.log"), "HumanSensor-1"),
        hs.HumanSensor(12, '10.10.2.126', 55550, getLogger("2"), os.path.join(logDir, "humanSensor.log"), "HumanSensor-2"),
        isend.ImageHandler('10.10.1.244', 50000, '10.10.2.126', 55550, getLogger("3"), os.path.join(logDir, "imageSender.log"), led_mac="A3:39:71:95:B0:BC", led_color="6c3cd4"),
    ]

    # スレッド処理するスレッドクラスの初期化
    threader = st.SensorThreader(sensors, 4)
    threader.start()


if __name__ == "__main__":
    main()
