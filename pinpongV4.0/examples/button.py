# -*- coding: utf-8 -*-

#实验效果：使用按钮控制arduino UNO板载亮灭
#接线：使用windows或linux电脑连接一块arduino主控板，主控板D8接一个按钮模块
import time
from pinpong.board import Board,Pin

board = Board("uno").begin()  #初始化，选择板型和端口号，不输入端口号则进行自动识别
#board = Board("uno","COM36").begin()  #windows下指定端口初始化
#board = Board("uno","/dev/ttyACM0").begin()   #linux下指定端口初始化
#board = Board("uno","/dev/cu.usbmodem14101").begin()   #mac下指定端口初始化

btn = Pin(Pin.D8, Pin.IN) #引脚初始化为电平输入
led = Pin(Pin.D13, Pin.OUT)

while True:
  v = btn.read_digital()  #读取引脚电平
  print(v)  #终端打印读取的电平状态
  led.write_digital(v)  #将按钮状态设置给led灯引脚
  time.sleep(0.1)
