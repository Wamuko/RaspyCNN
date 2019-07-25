import sys
graph_folder="./"
if sys.version_info.major < 3 or sys.version_info.minor < 4:
    print("Please using python3.4 or greater!")
    exit(1)

if len(sys.argv) > 1:
    graph_folder = sys.argv[1]

import picamera
import picamera.array
import numpy as np
import cv2
from mvnc import mvncapi as mvnc
from os import system
import io, time
import os.path
from datetime import datetime
from os.path import isfile, join
import re

import socket

LABELS = ('background',
          'aeroplane', 'bicycle', 'bird', 'boat',
          'bottle', 'bus', 'car', 'cat', 'chair',
          'cow', 'diningtable', 'dog', 'horse',
          'motorbike', 'person', 'pottedplant',
          'sheep', 'sofa', 'train', 'tvmonitor')

mvnc.SetGlobalOption(mvnc.GlobalOption.LOG_LEVEL, 2)
devices = mvnc.EnumerateDevices()
if len(devices) == 0:
    print("No devices found")
    quit()
print(len(devices))

devHandle   = []
graphHandle = []

# with open(join(graph_folder, "graph"), mode="rb") as f:
#     graph_buffer = f.read()
# graph = mvnc.Graph('MobileNet-SSD')

with open(join(graph_folder, "graph"), mode="rb") as f:
    graph = f.read()

for devnum in range(len(devices)):
    devHandle.append(mvnc.Device(devices[devnum]))
    devHandle[devnum].OpenDevice()
    graphHandle.append(devHandle[devnum].AllocateGraph(graph))
    graphHandle[devnum].SetGraphOption(mvnc.GraphOption.ITERATIONS, 1)
    iterations = graphHandle[devnum].GetGraphOption(mvnc.GraphOption.ITERATIONS)

print("\nLoaded Graphs!!!")

# 画像保存用ディレクトリの作成
segmented_images_dir = "saved_images"
current_images_dir = datetime.now().strftime("%Y%m%d_%H%M%S")
segmented_path = os.path.join(os.getcwd(), segmented_images_dir)
segmented_images_path = os.path.join(segmented_path, current_images_dir)
if not os.path.exists(segmented_images_path):
    os.makedirs(segmented_images_path)


# Configure depth and color streams
# pipeline = rs.pipeline()
# config = rs.config()
# config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
# config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

try:
    #freq = cv2.getTickFrequency()

    with picamera.PiCamera(resolution=(304, 304)) as camera:
        with picamera.array.PiRGBArray(camera) as stream:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                while(True):
                    # stream.arrayにRGBの順で映像データを格納
                    camera.capture(stream, 'bgr', use_video_port=True)

                    t1 = time.perf_counter()

                    # Wait for a coherent pair of frames: depth and color
                    if not stream:
                        continue

                    # Convert images to numpy arrays
                    #color_image = np.asanyarray(stream.array)

                    # サーバを指定
                    s.connect(('127.0.0.1', 50000))
                    # サーバにメッセージを送る
                    s.sendall(stream.array)
                    #
                    print('data sent')

                    if cv2.waitKey(1)&0xFF == ord('q'):
                        break
                    stream.seek(0)
                    stream.truncate()
except:
    import traceback
    traceback.print_exc()

finally:

    # Stop streaming
    for devnum in range(len(devices)):
        devHandle[devnum].CloseDevice()

    print("\n\nFinished\n\n")
    sys.exit()

