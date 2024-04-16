'''
Author: laplace825
Date: 2024-04-08 21:15:57
LastEditors: laplace825
LastEditTime: 2024-04-16 13:57:37
FilePath: /python/src/web.py
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
    def __init__(self) -> None:
        self.input_img_det_path = "" 
        self.output_det_dir = ""
        self.output_cls_result = ""
        pass

if __name__ == "__main__":
    print(f"\033[1;33mNow working on \033[1;31m{working_path}\033[0m")
    use_pt()
