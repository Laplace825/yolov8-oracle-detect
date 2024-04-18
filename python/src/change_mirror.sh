#!/bin/bash

echo > /etc/apt/sources.list

echo  "deb http://mirrors.tuna.tsinghua.edu.cn/debian/ buster main contrib non-free" >/etc/apt/sources.list
echo  "deb http://mirrors.tuna.tsinghua.edu.cn/debian/ buster-updates main contrib non-free" >>/etc/apt/sources.list
echo  "deb http://mirrors.tuna.tsinghua.edu.cn/debian/ buster-backports main contrib non-free" >>/etc/apt/sources.list
echo  "deb http://mirrors.tuna.tsinghua.edu.cn/debian-security buster/updates main contrib non-free" >>/etc/apt/sources.list