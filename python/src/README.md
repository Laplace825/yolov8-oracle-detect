<!--
 * @Author: laplace825
 * @Date: 2024-04-16 14:18:27
 * @LastEditors: laplace825
 * @LastEditTime: 2024-04-19 13:25:35
 * @FilePath: /python/src/README.md
 * @Description: 
 * 
 * Copyright (c) 2024 by laplace825, All Rights Reserved. 
-->
# YOLOv8 Python API with FastApi

`__pycache__` 可以忽略

```
src
├── api.py
├── cls.py
├── det.py
├── infer.py
├── onnx
│   ├── best_cls.onnx
│   └── best_det.onnx
├── pt
│   ├── best_cls.pt
│   └── best_det.pt
├── __pycache__
│   ├── api.cpython-310.pyc
│   ├── cls.cpython-310.pyc
│   ├── det.cpython-310.pyc
│   └── infer.cpython-310.pyc
├── README.md
└── upload_img
    ├── 2024-04-13_16-34-48
    │   ├── b00762.jpg 
    │   └── output_img
    │       └── 0 
    │           ├── b00762_0.jpg
    │           ├── b00762_10.jpg
    │           ├── b00762_11.jpg
    │           ├── b00762_1.jpg
    │           ├── b00762_2.jpg
    │           ├── b00762_3.jpg
    │           ├── b00762_4.jpg
    │           ├── b00762_5.jpg
    │           ├── b00762_6.jpg
    │           ├── b00762_7.jpg
    │           ├── b00762_8.jpg
    │           ├── b00762_9.jpg
    │           ├── cls
    │           │   ├── b00762_0.txt
    │           │   ├── b00762_10.txt
    │           │   ├── b00762_11.txt
    │           │   ├── b00762_1.txt
    │           │   ├── b00762_2.txt
    │           │   ├── b00762_3.txt
    │           │   ├── b00762_4.txt
    │           │   ├── b00762_5.txt
    │           │   ├── b00762_6.txt
    │           │   ├── b00762_7.txt
    │           │   ├── b00762_8.txt
    │           │   └── b00762_9.txt
    │           └── det
    │               └── b00762.jpg
    └── 2024-04-13_16-38-07
        ├── 41_F57A-1.jpg 
        └── output_img
            └── 0
                └── cls
                    └── 41_F57A-1.txt
```