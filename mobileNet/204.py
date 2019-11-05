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
        isend.ImageHandler('172.16.202.1', 50000, '0.0.0.0', 55550, getLogger("4"), os.path.join(logDir, "imageSender.log"), led_mac="27:A3:A2:F9:49:98", led_color="6c3cd4"),
    ]

    # スレッド処理するスレッドクラスの初期化
    threader = st.SensorThreader(sensors, 4)
    threader.start()


if __name__ == "__main__":
    main()
