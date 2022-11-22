# -*- coding: utf-8 -*-

import time
from pinpong.board import Board
from pinpong.extension.handpy import *
from pinpong.libs.microbit_motor import DFServo 

Board("handpy").begin()  #初始化，选择板型和端口号，不输入端口号则进行自动识别
#Board("handpy","COM36").begin()  #windows下指定端口初始化
#Board("handpy","/dev/ttyACM0").begin()   #linux下指定端口初始化
#Board("handpy","/dev/cu.usbmodem14101").begin()   #mac下指定端口初始化

S8 = DFServo(8)

while True:
    S8.angle(45)
    sleep_ms(1000)
    S8.angle(145)
    sleep_ms(1000)
