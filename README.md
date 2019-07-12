# RaspyCNN
MobileNet+Movidiusを用いてラズパイカメラを使って動画を継続的にセグメンテーションするプロジェクト
当初はMask R-CNNで試すつもりだったが、そもそもモデルサイズが大きすぎたため断念している。

# 使い方
cd mobileNet
python3 SingleSSDwithPiCamera.py

# 環境
mvnc v.1 (v.2での使用は不可能です)
python 3.5
PiCamera
ラズパイ 3B+

# 概要
PiCameraから撮影した画像に対してMobileNetを使用して、出力をjpg方式で保存します。
保存は10Frame間隔で行われます。私の環境では6FPS程度の速度で動作しました。

# 参考にしたサイト
1.Mask R-CNNを簡単にカメラ映像から試す方法
https://ai-coordinator.jp/mask-r-cnn#i
