# -*- coding: utf-8 -*-

#实验效果：控制microbit板载LED灯一秒闪烁一次
#接线：使用windows或linux电脑连接一块microbit主控板
import time
from pinpong.board import Board,Pin

Board("microbit").begin()               #初始化，选择板型和端口号，不输入端口号则进行自动识别
#Board("microbit","COM36").begin()      #windows下指定端口初始化
#Board("microbit","/dev/ttyACM0").begin() #linux下指定端口初始化
#Board("microbit","/dev/cu.usbmodem14101").begin()   #mac下指定端口初始化

led = Pin(Pin.P0, Pin.OUT) #引脚初始化为电平输出

while True:
  led.write_digital(1) #输出高电平
  time.sleep(1) #等待1秒 保持状态

  led.write_digital(0) #输出低电平
  time.sleep(1) #等待1秒 保持状态
