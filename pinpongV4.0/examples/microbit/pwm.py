# -*- coding: utf-8 -*-

#实验效果：使用按钮控制LED模块亮度
#接线：使用windows或linux电脑连接一块arduino主控板，主控板P16接一个LED灯模块
import time
from pinpong.board import Board,Pin,PWM #导入PWM类实现模拟输出

Board("").begin()  #初始化，选择板型和端口号，不输入端口号则进行自动识别
#Board("microbit","COM36").begin()  #windows下指定端口初始化
#Board("microbit","/dev/ttyACM0").begin()   #linux下指定端口初始化
#Board("microbit","/dev/cu.usbmodem14101").begin()   #mac下指定端口初始化

pwm0 = PWM(Pin(Pin.P2)) #将Pin传入PWM中实现模拟输出  引脚有P0,P1,P5,P6,P7,P8,P9,P11,P13,P14,P15,P16

while True:
  j = 0
  for i in range(1024): #从0到1023循环
    j += 50
    if j == 1000:
      break
    pwm0.duty(j)  #设置模拟输出值
    print(j)
    time.sleep(0.05)
