# -*- coding: UTF-8 -*-
import cv2
import cls
import det
import sys
import os
import tqdm
from ultralytics import YOLO

input_img_det_path = "/home/lap/app/AI/YOLOv8/ultralytics/deploy/python/input_img/"


def use_onnx():
    net_det_path = "/home/lap/app/AI/YOLOv8/ultralytics/deploy/python/best_det.onnx"
    output_det_img_path = (
        "/home/lap/app/AI/YOLOv8/ultralytics/deploy/python/output_text_img_onnx/"
    )

    net_cls_path = "/home/lap/app/AI/YOLOv8/ultralytics/deploy/python/best_cls.onnx"
    input__img_cls_path = (
        "/home/lap/app/AI/YOLOv8/ultralytics/deploy/python/output_text_img_onnx/"
    )
    class_name_path = "/home/lap/app/AI/YOLOv8/ultralytics/deploy/python/class_cls.txt"
    output_cls_txt_path = (
        "/home/lap/app/AI/YOLOv8/ultralytics/deploy/python/output_cls.txt"
    )
    # 读取input_img下所有图片，进行检测和分类

    for file in tqdm.tqdm(os.listdir(input_img_det_path), desc="Detecting"):
        if file.endswith(".jpg") or file.endswith(".png"):
            img_path = os.path.join(input_img_det_path, file)
            det.det(
                net_det_path,
                img_path,
                output_det_img_path,
            )
    print(">>>> Classfiying...\n")
    # 分类
    cls.cls(
        net_cls_path,
        input__img_cls_path,
        class_name_path,
        output_cls_txt_path,
    )
    print(f"Done! cls result saved at {output_cls_txt_path}")


def use_pt():
    pt_det_path = "/home/lap/app/AI/YOLOv8/ultralytics/deploy/python/best_det.pt"
    output_det_dir = "/home/lap/app/AI/YOLOv8/ultralytics/deploy/python/output_img_pt"
    pt_cls_path = "/home/lap/app/AI/YOLOv8/ultralytics/deploy/python/best_cls.pt"
    output_cls_result = "/home/lap/app/AI/YOLOv8/ultralytics/deploy/python/output_img_pt/0/cls"
    det.det_yolo(
        pt_det_path,
        input_img_det_path,
        output_det_dir,
    )
    cls.cls_yolo(
        pt_cls_path,
        output_det_dir + "/0",
        output_cls_result,
    )


if __name__ == "__main__":
    use_pt() 
