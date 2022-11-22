# -*- coding: utf-8 -*-
import time
from pinpong.board import Board
from pinpong.libs.dfrobot_ozone import Ozone

Board("uno").begin()#初始化，选择板型和端口号，不输入端口号则进行自动识别
#Board("uno","COM36").begin()  #windows下指定端口初始化
#Board("uno","/dev/ttyACM0").begin()   #linux下指定端口初始化
#Board("uno","/dev/cu.usbmodem14101").begin()   #mac下指定端口初始化

oz = Ozone(0x70)
#设置模式主动或者被动模式, MEASURE_MODE_AUTOMATIC,MEASURE_MODE_PASSIVE
oz.set_mode(oz.MEASURE_MODE_AUTOMATIC)
collection_times = 20
while True:
    value = oz.read_ozone_data(collection_times)
    print("ozone concentration is %d PPB" %value)
    time.sleep(1)