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
            output = np.empty((300 * 300 * 3,), dtype=np.uint8)
            frames = 0
            while(True):
                # stream.arrayにRGBの順で映像データを格納
                camera.capture(stream, 'bgr', use_video_port=True)

                t1 = time.perf_counter()

                # Wait for a coherent pair of frames: depth and color
                if not stream:
                    continue

                # Convert images to numpy arrays
                color_image = np.asanyarray(stream.array)
                #dnn
                im = cv2.resize(color_image, (300, 300))
                im = im - 127.5
                im = im * 0.007843

                #graphHandle[0][0]=input_fifo, graphHandle[0][1]=output_fifo
                graphHandle[0].LoadTensor(im.astype(np.float16), None)
                out, input_image = graphHandle[0].GetResult()

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
                        if (percentage <= min_score_percent):
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
                    cv2.imwrite(os.path.join(segmented_images_path, str(frames)) + '.jpg', color_image)
                frames += 1

                ## Print FPS
                t2 = time.perf_counter()
                time1 = (t2-t1)#/freq
                print(" {:.2f} FPS".format(1/time1))

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

