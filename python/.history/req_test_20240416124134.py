'''
Author: laplace825
Date: 2024-04-12 16:52:14
LastEditors: laplace825
LastEditTime: 2024-04-16 12:41:12
FilePath: /python/req_test.py
Description: 

Copyright (c) 2024 by laplace825, All Rights Reserved. 
'''


import requests
import socket



if __name__ == "__main__":
    sock = socket.socket()
    sock.bind(("127.0.0.1", 8000))
    sock.listen(5)
    repos = requests.get("http://localhost:8000/people/1")
    print(repos.json())

