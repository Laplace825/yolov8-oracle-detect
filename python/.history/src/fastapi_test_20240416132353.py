"""
Author: laplace825
Date: 2024-04-12 15:45:16
LastEditors: laplace825
LastEditTime: 2024-04-16 13:00:51
FilePath: /python/fastapi_test.py
Description: 

Copyright (c) 2024 by laplace825, All Rights Reserved. 
"""

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import shutil
import uvicorn
from typing import Optional
from pydantic import BaseModel
import os
import sys
from datetime import datetime
import det
import cls



app = FastAPI()

# 当前工作区上一级文件夹
# .../python/
working_space = os.path.abspath(os.path.dirname(os.path.dirname(sys.argv[0])))
# 用户上传文件的目录
# NOTE: 在该目录下按上传时间新建文件夹,将上传的文件保存到该文件夹
upload_loader = working_space + "/test_img"

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

@app.get("/")
def index():
    return {"message": "FastAPI !"}

# 提交文件
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # 根据当前上传时间新建文件夹，并把文件保存到该文件夹
        current_time = datetime.now()
        time_str = current_time.strftime("%Y-%m-%d_%H-%M-%S")
        new_folder_path = os.path.join(upload_loader, time_str)
        os.makedirs(new_folder_path, exist_ok=True)

        file_path = os.path.join(new_folder_path, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return JSONResponse(content={"message": "Upload file success!"})
    except Exception as e:
        print(f"error : {e}")
        return JSONResponse(
            status_code=500, content={"message": "An error occured, upload_file"}
        )


if __name__ == "__main__":
    uvicorn.run(app="fastapi_test:app", host="0.0.0.0", port=8000, reload=True)
