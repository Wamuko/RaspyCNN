# -*- coding: utf-8 -*-
import sys

graph_folder = "./"
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


# センサーと同じように非同期処理で走らせるので、superクラスをimplementする形の方がよかったかも
class SSD:
    def __init__(self, ip_from, port_from):
        self.IS_WORKING = False
        self.ip_from = ip_from
        self.port_from = port_from
        self.LABELS = ('background',
                  'aeroplane', 'bicycle', 'bird', 'boat',
                  'bottle', 'bus', 'car', 'cat', 'chair',
                  'cow', 'diningtable', 'dog', 'horse',
                  'motorbike', 'person', 'pottedplant',
                  'sheep', 'sofa', 'train', 'tvmonitor')

        mvnc.SetGlobalOption(mvnc.GlobalOption.LOG_LEVEL, 2)
        self.devices = mvnc.EnumerateDevices()
        if len(self.devices) == 0:
            print("No devices found")
            quit()
        print(len(self.devices))

        self.devHandle = []
        self.graphHandle = []

        # with open(join(graph_folder, "graph"), mode="rb") as f:
        #     graph_buffer = f.read()
        # graph = mvnc.Graph('MobileNet-SSD')

        with open(join(graph_folder, "graph"), mode="rb") as f:
            graph = f.read()

        for devnum in range(len(self.devices)):
            self.devHandle.append(mvnc.Device(self.devices[devnum]))
            self.devHandle[devnum].OpenDevice()
            self.graphHandle.append(self.devHandle[devnum].AllocateGraph(graph))
            self.graphHandle[devnum].SetGraphOption(mvnc.GraphOption.ITERATIONS, 1)
            iterations = self.graphHandle[devnum].GetGraphOption(mvnc.GraphOption.ITERATIONS)

        print("\nLoaded Graphs!!!")

        # 画像保存用ディレクトリの作成
        segmented_images_dir = "saved_images"
        current_images_dir = datetime.now().strftime("%Y%m%d_%H%M%S")
        segmented_path = os.path.join(os.getcwd(), segmented_images_dir)
        self.segmented_images_path = os.path.join(segmented_path, current_images_dir)
        if not os.path.exists(self.segmented_images_path):
            os.makedirs(self.segmented_images_path)

    def start(self, executor):
        return executor.submit(fn=self.work)

    def work(self):
        if self.IS_WORKING:
            return
        else:
            self.IS_WORKING = True
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # IPアドレスとポートを指定
                s.bind((self.ip_from, self.port_from))
                # 1 接続
                s.listen(1)
                # connection するまで待つ
                while True:
                    # 誰かがアクセスしてきたら、コネクションとアドレスを入れる
                    conn, addr = s.accept()
                    with conn:
                        frames = 0
                        while True:
                            # データを受け取る
                            data = conn.recv(300*300*3)
                            if not data:
                                continue

                            print('received')

                            # Convert images to numpy array
                            encoded = np.fromstring(data, np.uint8)
                            np_encoded = np.reshape(encoded, (300, 300, 3))
                            color_image = cv2.imdecode(np_encoded, cv2.IMREAD_COLOR)
                            # dnn
                            im = cv2.resize(color_image, (300, 300))
                            im = im - 127.5
                            im = im * 0.007843

                            # self.graphHandle[0][0]=input_fifo, self.graphHandle[0][1]=output_fifo
                            self.graphHandle[0].LoadTensor(im.astype(np.float16), None)
                            out, input_image = self.graphHandle[0].GetResult()

                            # Show images
                            height = color_image.shape[0]
                            width = color_image.shape[1]
                            num_valid_boxes = int(out[0])

                            if num_valid_boxes > 0:

                                for box_index in range(num_valid_boxes):
                                    base_index = 7 + box_index * 7
                                    if (not np.isfinite(out[base_index]) or
                                        not np.isfinite(out[base_index + 1]) or
                                        not np.isfinite(out[base_index + 2]) or
                                        not np.isfinite(out[base_index + 3]) or
                                        not np.isfinite(out[base_index + 4]) or
                                        not np.isfinite(out[base_index + 5]) or
                                        not np.isfinite(out[base_index + 6])):
                                        continue

                                    x1 = max(0, int(out[base_index + 3] * height))
                                    y1 = max(0, int(out[base_index + 4] * width))
                                    x2 = min(height, int(out[base_index + 5] * height))
                                    y2 = min(width, int(out[base_index + 6] * width))

                                    object_info_overlay = out[base_index:base_index + 7]

                                    min_score_percent = 60
                                    source_image_width = width
                                    source_image_height = height

                                    base_index = 0
                                    class_id = object_info_overlay[base_index + 1]
                                    percentage = int(object_info_overlay[base_index + 2] * 100)
                                    if percentage <= min_score_percent:
                                        continue

                                    box_left = int(object_info_overlay[base_index + 3] * source_image_width)
                                    box_top = int(object_info_overlay[base_index + 4] * source_image_height)
                                    box_right = int(object_info_overlay[base_index + 5] * source_image_width)
                                    box_bottom = int(object_info_overlay[base_index + 6] * source_image_height)
                                    label_text = LABELS[int(class_id)] + " (" + str(percentage) + "%)"

                                    box_color = (255, 128, 0)
                                    box_thickness = 1
                                    cv2.rectangle(color_image, (box_left, box_top), (box_right, box_bottom), box_color, box_thickness)

                                    label_background_color = (125, 175, 75)
                                    label_text_color = (255, 255, 255)

                                    label_size = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
                                    label_left = box_left
                                    label_top = box_top - label_size[1]
                                    if (label_top < 1):
                                        label_top = 1
                                    label_right = label_left + label_size[0]
                                    label_bottom = label_top + label_size[1]
                                    cv2.rectangle(color_image, (label_left - 1, label_top - 1), (label_right + 1, label_bottom + 1), label_background_color, -1)
                                    cv2.putText(color_image, label_text, (label_left, label_bottom), cv2.FONT_HERSHEY_SIMPLEX, 0.5, label_text_color, 1)

                            # cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
                            # cv2.imshow('RealSense', cv2.resize(color_image,(width, height)))

                            # ディレクトリにJPGイメージを保存する
                            if frames % 10 == 0:
                                cv2.imwrite(os.path.join(self.segmented_images_path, str(frames)) + '.jpg', color_image)
                            frames += 1

                            ## Print FPS
                            t2 = time.perf_counter()
                            time1 = (t2-t1)#/freq
                            print(" {:.2f} FPS".format(1/time1))

                            if cv2.waitKey(1)&0xFF == ord('q'):
                                break
        except:
            import traceback
            traceback.print_exc()

        finally:

            # Stop streaming
            for devnum in range(len(self.devices)):
                self.devHandle[devnum].CloseDevice()

            print("\n\nFinished\n\n")
            sys.exit()
