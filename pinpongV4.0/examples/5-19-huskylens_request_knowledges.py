# -*- coding: utf-8 -*-

#实验效果：加载或保存模型
#接线：使用windows或linux电脑连接一块arduino主控板，哈士奇接到I2C口SCL SDA
import time
from pinpong.board import Board
from pinpong.libs.dfrobot_huskylens import Huskylens

Board("uno").begin()  #初始化，选择板型和端口号，不输入端口号则进行自动识别
#Board("uno","COM36").begin()  #windows下指定端口初始化
#Board("uno","/dev/ttyACM0").begin()   #linux下指定端口初始化
#Board("uno","/dev/cu.usbmodem14101").begin()   #mac下指定端口初始化

husky = Huskylens()

file_index = 1
#保存模型 
# 如果是物体追踪模式下保存的模型，名称为： ObjectTracking_Backup_1.bin
# husky.command_request_save_model_to_SD_card(file_index)
# time.sleep(2)
#加载模型
husky.command_request_load_model_from_SD_card(file_index)
time.sleep(2)









