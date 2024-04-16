<!--
 * @Author: laplace825
 * @Date: 2024-04-16 14:18:27
 * @LastEditors: laplace825
 * @LastEditTime: 2024-04-16 14:28:51
 * @FilePath: /python/src/README.md
 * @Description: 
 * 
 * Copyright (c) 2024 by laplace825, All Rights Reserved. 
-->
# YOLOv8 Python API with FastApi

`__pycache__` 可以忽略

```
src
├── cls.py
├── det.py
├── fastapi_test.py
├── infer.py
├── onnx
│   ├── best_cls.onnx
│   └── best_det.onnx
├── pt
│   ├── best_cls.pt
│   └── best_det.pt
├── __pycache__
│   ├── cls.cpython-310.pyc
│   ├── det.cpython-310.pyc
│   ├── fastapi_test.cpython-310.pyc
│   └── infer.cpython-310.pyc
├── README.md
└── upload_img (存放图片文件夹)
    └── 2024-04-16_14-17-40 (根据用户上传时间将图片存放单独的文件夹)
        ├── b00920Z.jpg (用户上传的图片)
        └── output_img_pt (推理输出文件夹)
            └── 0 (图片分割后的文件夹)
                ├── b00920Z_02.jpg
                ├── b00920Z_03.jpg
                ├── b00920Z_04.jpg
                ├── b00920Z_0.jpg
                └── cls (分类结果)
                    ├── b00920Z_02.txt
                    ├── b00920Z_03.txt
                    ├── b00920Z_04.txt
                    └── b00920Z_0.txt
```