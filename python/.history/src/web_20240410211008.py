# -*- coding: UTF-8 -*-
import cv2
import cls
import det
import sys
import os
import tqdm
from ultralytics import YOLO

# 获取 python 文件目录
# ../python/src
working_path = os.path.abspath(os.path.dirname(os.path.dirname(sys.argv[0])))

input_img_det_path = working_path + "/input_img/"


def use_onnx():
    net_det_path = working_path + "/best_det.onnx"
    output_det_img_path = working_path + "/output_text_img_onnx/"

    net_cls_path = working_path + "/best_cls.onnx"
    input__img_cls_path = working_path + "/output_text_img_onnx/"
    class_name_path = working_path + "/class_cls.txt"
    output_cls_txt_path = working_path + "/output_cls.txt"
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
    pt_det_path = working_path + "/best_det.pt"
    output_det_dir = working_path + "/output_img_pt"
    pt_cls_path = working_path + "/best_cls.pt"
    output_cls_result = working_path + "/output_img_pt/0/cls"
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
    print(
        f"""\033[1;33mDone! cls result save in \033[1;31m{output_cls_result}\033[0m
\033[1;33mdet result after cropping save in \033[1;31m{output_det_dir + "/0"}\033[0m"""
    )


if __name__ == "__main__":
    print(f"\033[1;33mNow working on \033[1;31m{working_path}\033[0m")
    use_pt()
