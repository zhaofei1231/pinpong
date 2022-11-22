# -*- coding: utf-8 -*-
#实验效果：展示红外接收功能
#接线：handpy支持
import sys
import time
from pinpong.board import Board,IRRecv,Pin

Board("handpy").begin()  #初始化，选择板型和端口号，不输入端口号则进行自动识别
#Board("handpy","COM36").begin()  #windows下指定端口初始化
#Board("handpy","/dev/ttyACM0").begin()   #linux下指定端口初始化
#Board("handpy","/dev/cu.usbmodem14101").begin()   #mac下指定端口初始化


def ir_recv3(data):
  print("------P0--------")
  print(hex(data))

#ir2 = IRRecv(Pin(0))
ir3 = IRRecv(Pin(0),ir_recv3)

while(1):
#  v = ir2.read()
#  if v:
#   print("------P2--------")
#   print(hex(v))
  time.sleep(0.1)