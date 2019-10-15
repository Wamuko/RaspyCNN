# -*- coding: utf-8 -*-
import sys, os

if sys.version_info.major < 3 or sys.version_info.minor < 4:
    print("Please using python3.4 or greater!")
    exit(1)

from packs import humanSensor as hs
from packs import imageHandler as isend
from packs import sensorThreader as st
from logging import getLogger


def main():
    # ログ作成用初期処理
    logger = getLogger("sensors")
    logDir = os.path.join(os.getcwd(), "log")
    if not os.path.exists(logDir):
        os.mkdir(logDir)

    # センサーの定義
    sensors = [
        hs.HumanSensor(18, '10.10.1.224', 6666, logger, os.path.join(logDir, "humanSensor.log"), "HumanSensor"),
        isend.ImageHandler('10.10.1.224', 5000, 6666, logger, os.path.join(logDir, "sender.log"))
    ]
    # 画像送信クラスの初期化

    # スレッド処理するスレッドクラスの初期化
    threader = st.SensorThreader(sensors, 4)


if __name__ == "__main__":
    main()
