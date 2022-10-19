# -*- coding: utf-8 -*-

#实验效果：读取I2C CCS811空气质量传感器
#接线：使用windows或linux电脑连接一块arduino主控板，空气质量传感器接到I2C口SCL SDA
import time
from pinpong.board import Board
from pinpong.libs.dfrobot_ccs811 import CCS811, CCS811_Ecycle, CCS811_Emode


ip = "192.168.0.90"
port = 8081

Board(ip, port)

ccs811 = CCS811()

#ccs811.write_base_line(baseline)                  #获取到的基线填入
while True:
    if(ccs811.check_data_ready()):
        print("---------------------")
        print("CO2:"+str(ccs811.CO2_PPM())+" ppm")
        print("TVOC:"+str(ccs811.TVOC_PPB())+" ppb")
        print("---------------------")
    else:
        print("data is not ready!")
    time.sleep(1)