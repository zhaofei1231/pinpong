# -*- coding: utf-8 -*-

#实验效果：读取I2C CCS811空气质量传感器
#接线：使用windows或linux电脑连接一块handpy主控板，空气质量传感器接到I2C口SCL SDA
import time
from pinpong.board import Board
from pinpong.libs.dfrobot_ccs811 import CCS811, CCS811_Ecycle, CCS811_Emode


Board("handpy").begin()  #初始化，选择板型和端口号，不输入端口号则进行自动识别
#Board("handpy","COM36").begin()  #windows下指定端口初始化
#Board("handpy","/dev/ttyACM0").begin()   #linux下指定端口初始化
#Board("handpy","/dev/cu.usbmodem14101").begin()   #mac下指定端口初始化

ccs811 = CCS811()

ccs811.write_base_line(0xb47f)                  #获取到的基线填入
while True:
    if(ccs811.check_data_ready()):
        print("CO2:"+str(ccs811.CO2_PPM())+" ppm")
        print("TVOC:"+str(ccs811.TVOC_PPB())+" ppb")
    else:
        print("data is not ready!")
    time.sleep(1)