"""
Author: laplace825
Date: 2024-04-08 22:12:00
LastEditors: laplace825
LastEditTime: 2024-04-17 16:56:09
FilePath: /python/src/cls.py
Description: 

Copyright (c) 2024 by laplace825, All Rights Reserved. 
"""
import cv2
import numpy as np
import os
import tqdm
from ultralytics import YOLO

# Constants
INPUT_WIDTH = 416
INPUT_HEIGHT = 416


# Preprocessing function
def pre_process(image):
    # CenterCrop: Crop the image to a square and resize it to match the network input
    crop_size = min(image.shape[0], image.shape[1])
    left = (image.shape[1] - crop_size) // 2
    top = (image.shape[0] - crop_size) // 2
    crop_image = image[top : top + crop_size, left : left + crop_size]
    crop_image = cv2.resize(crop_image, (INPUT_WIDTH, INPUT_HEIGHT))

    # Normalize: Normalize the image to the range of 0-1, subtract mean, and divide by standard deviation
    crop_image = crop_image.astype(np.float32) / 255.0
    crop_image = (crop_image - np.array([0.406, 0.456, 0.485])) / np.array(
        [0.225, 0.224, 0.229]
    )

    # Convert theprocessed image to blob format accepted by the network
    crop_image = cv2.convertScaleAbs(crop_image)
    blob = cv2.dnn.blobFromImage(
        crop_image, 1.0, (INPUT_WIDTH, INPUT_HEIGHT), (0, 0, 0), swapRB=True, crop=False
    )

    return blob


# Network inference function
def process(blob, net):
    # Set the network input
    net.setInput(blob)
    # Perform forward pass and get the outputs
    outputs = net.forward(net.getUnconnectedOutLayersNames())

    return outputs


# Postprocessing function
def post_process(detections, class_name):
    values = detections[0][0]
    id = np.argmax(values)

    return class_name[id]


def cls(onnx_model_path, input_image_dir, class_name_path, output_txt_path):
    class_name = []
    with open(class_name_path, "r") as file:
        for line in file:
            class_name.append(line.strip())

    # Load the ONNX model
    onnx_model = cv2.dnn.readNet(onnx_model_path)

    # Set the network backend and target to CUDA
    onnx_model.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    onnx_model.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    input_dir = input_image_dir
    # Iterate through the input image directory, preprocess and perform network inference on each image, and write the results to a file
    with open(output_txt_path, "w") as out_file:
        for entry in tqdm.tqdm(os.scandir(input_dir), desc="Classifying"):
            image = cv2.imread(entry.path)
            blob = pre_process(image)
            outputs = process(blob, onnx_model)
            result = post_process(outputs, class_name)
            # 打印图片路径和分类结果
            # print(entry.path, ":", result)
            out_file.write(entry.path.split("/")[-1] + " : " + result + "\n")


def cls_yolo(pt_path, input_image_dir, output_txt_dir):
    if pt_path.endswith(".onnx"):
        raise ValueError("pt_path must be a .pt file")
    model = YOLO(pt_path)
    for file in os.listdir(input_image_dir):
        if file.endswith(".jpg") or file.endswith(".png"):
            img_path = os.path.join(input_image_dir, file)
            result = model(img_path)
            for res in result:
                res.save_txt(
                    f"{output_txt_dir}/{img_path.split('/')[-1].split('.')[0]}.txt"
                )


# Main function
if __name__ == "__main__":
    pass
