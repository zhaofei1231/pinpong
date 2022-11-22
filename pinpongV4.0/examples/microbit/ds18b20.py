# -*- coding: utf-8 -*-

#实验效果：读取DS18B20防水温度传感器
#接线：使用windows或linux电脑连接一块MICROBIT主控板
import time
from pinpong.board import Board,Pin,DS18B20

Board("microbit").begin()  #初始化，选择板型和端口号，不输入端口号则进行自动识别
#Board("microbit","COM36").begin()  #windows下指定端口初始化
#Board("microbit","/dev/ttyACM0").begin()   #linux下指定端口初始化
#Board("microbit","/dev/cu.usbmodem14101").begin()   #mac下指定端口初始化

ds18b20 = DS18B20(Pin(Pin.P1))

while True:
  temp = ds18b20.temp_c()
  print("temperature = ",temp)
  time.sleep(0.5)














