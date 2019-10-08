# -*- coding: utf-8 -*-
import sys, os

if sys.version_info.major < 3 or sys.version_info.minor < 4:
    print("Please using python3.4 or greater!")
    exit(1)

from packs import humanSensorReader as hs
from packs import imageSender as isend
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
        hs.HumanSensorReader(18, logger, "humanSensor", "HumanSensor"),
    ]

    # 画像送信クラスの初期化
    imageSender = isend.ImageSender('172.16.202.1', 50000)

    # スレッド処理するスレッドクラスの初期化
    threader = st.SensorThreader(sensors, 4)

    # センサーの値の取得とlogへの書き出しを開始
    threader.start()

    # ログを見て、もしくは何らかのイベントで画像送信クラスを下記のようにスタートさせないといけないが
    # どうやればいいか考え中
    # imageSender.start()

if __name__ == "__main__":
    main()
