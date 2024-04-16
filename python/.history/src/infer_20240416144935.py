'''
Author: laplace825
Date: 2024-04-08 21:15:57
LastEditors: laplace825
LastEditTime: 2024-04-16 14:49:35
FilePath: /python/src/infer.py
Description: 

Copyright (c) 2024 by laplace825, All Rights Reserved. 
'''

# -*- coding: UTF-8 -*-
import cv2
import cls
import det
import sys
import os
import tqdm
from ultralytics import YOLO


class Inference:
    def __init__(self, working_space) -> None:
        self.working_space = working_space
        self.uplaod_loader = working_space + "/upload_img"

    def use_onnx(
        self,
        input_img_det_path,
        output_det_img_path,
        input__img_cls_path,
        output_cls_txt_path,
    ):
        """
        description: 使用onnx模型进行检测和分类
        param {*} output_det_img_path: 检测结果保存路径
        param {*} input_img_cls_path: 分类输入图片路径
        param {*} output_cls_txt_path: 分类结果保存路径 保存格式为：图片名:分类结果
        return {*}
        """
        net_det_path = self.working_space + "/onnx/best_det.onnx"
        net_cls_path = self.working_space + "/onnx/best_cls.onnx"
        class_name_path = self.working_space + "/class_cls.txt"  # 分类类别文件

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

    def use_pt_det(self, input_img_det_path, output_det_dir):
        """
        param {*} input_img_det_path: 检测输入图片路径
        param {*} output_det_dir: 检测结果保存路径
        param {*} output_cls_result: 分类结果保存路径
        NOTE: 注意output_det_dir下会生成一个0文件夹,存放检测结果
        return {*}
        """
        pt_det_path = self.working_space + "/pt/best_det.pt"

        det.det_yolo(
            pt_det_path,
            input_img_det_path,
            output_det_dir,
        )

    def use_pt_cls(self, output_det_dir, output_cls_result):
        pt_cls_path = self.working_space + "/pt/best_cls.pt"
        cls.cls_yolo(
            pt_cls_path,
            output_det_dir，
            output_cls_result,
        )
        print(
            f"""\033[1;33mDone! cls result save in \033[1;31m{output_cls_result}\033[0m
    \033[1;33mdet result after cropping save in \033[1;31m{output_det_dir + "/0"}\033[0m"""
        )


if __name__ == "__main__":
    print(f"\033[1;33mNow working")
