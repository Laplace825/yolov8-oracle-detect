"""
Author: laplace825
Date: 2024-04-12 16:52:14
LastEditors: laplace825
LastEditTime: 2024-04-16 12:42:45
FilePath: /python/req_test.py
Description: 

Copyright (c) 2024 by laplace825, All Rights Reserved. 
"""

import requests
import socket


if __name__ == "__main__":
    url = "localhost:8000/upload"
    repos = requests.post(url, files={"file": open("req_test.py", "rb")})
    print(repos.text)
