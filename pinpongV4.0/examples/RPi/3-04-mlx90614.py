# -*- coding: utf-8 -*-

##RPi and PythonBoard
#实验效果：读取I2C MLX90614远红外测温传感器

import time
from pinpong.board import Board
from pinpong.libs.dfrobot_mlx90614 import MLX90614 #从libs导入mlx90614库

Board("RPi").begin()

irt=MLX90614(bus_num = 1)                      

while True:
  print("Object  %s *C"% irt.obj_temp_c())     #读取物体温度 摄氏度（℃）
  print("Object  %s *F"% irt.obj_temp_f())     #读取物体温度 华氏度（℉）
  print("Ambient %s *C"% irt.env_temp_c())     #读取环境温度 摄氏度（℃）
  print("Ambient %s *F"% irt.env_temp_f())     #读取环境温度 华氏度（℉）
  print() #空行 
  time.sleep(1)
