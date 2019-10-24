# -*- coding: utf-8 -*-
import sys, os
from socket import socket, AF_INET, SOCK_DGRAM

if sys.version_info.major < 3 or sys.version_info.minor < 4:
    print("Please using python3.4 or greater!")
    exit(1)

import SSD as sd
from packs import sensorThreader as st
from logging import getLogger


def main():
    # ログ作成用初期処理
    logDir = os.path.join(os.getcwd(), "log")
    if not os.path.exists(logDir):
        os.mkdir(logDir)

    # センサーの定義
    sensors = [
        sd.SSD('0.0.0.0', 50000),
    ]

    # スレッド処理するスレッドクラスの初期化
    threader = st.SensorThreader(sensors, 4)
    threader.start()


if __name__ == "__main__":
    main()
