# -*- coding: utf-8 -*-

#NeZha 
#实验效果：控制板载LED灯一秒闪烁一次

import time
from pinpong.board import Board,Pin

Board("nezha").begin()

led = Pin(25, Pin.OUT) #Nezha引脚初始化为电平输出

while True:
  led.value(1) #输出高电平
  print("1") #终端打印信息
  time.sleep(1) #等待1秒 保持状态

  led.value(0) #输出低电平
  print("0") #终端打印信息
  time.sleep(1) #等待1秒 保持状态
