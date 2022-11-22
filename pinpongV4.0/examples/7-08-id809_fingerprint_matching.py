# -*- coding: utf-8 -*-
import time
from pinpong.board import Board,Pin
from pinpong.libs.dfrobot_id809 import ID809

Board("uno").begin()#初始化，选择板型和端口号，不输入端口号则进行自动识别
#Board("uno","COM36").begin()  #windows下指定端口初始化
#Board("uno","/dev/ttyACM0").begin()   #linux下指定端口初始化
#Board("uno","/dev/cu.usbmodem14101").begin()   #mac下指定端口初始化

fingerprint = ID809()

while fingerprint.connected() == False:
    print("Communication with device failed, please check connection")
    time.sleep(1)

while True:
#   ctrl_led参数1:<LEDMode>
#   breathing   fast_blink   keeps_on    normal_close
#   fade_in      fade_out     slow_blink   
#   ctrl_led参数2:<LEDColor>
#   green  red      yellow   blue
#   cyan   magenta  white
#   ctrl_led参数3:<呼吸、闪烁次数> 0表示一直呼吸、闪烁，
#   该参数仅breathing、fast_blink、slow_blink模式下有效
    fingerprint.ctrl_led(fingerprint.breathing, fingerprint.blue, 0)
    print("请按下手指")
    if fingerprint.collection_fingerprint(10) != fingerprint.error:
        fingerprint.ctrl_led(fingerprint.fast_blink, fingerprint.yellow, 3)
        print("采集成功")
        print("请松开手指")
        while fingerprint.detect_finger():pass
        ret = fingerprint.search()   #将采集到的指纹与指定编号指纹对比,成功返回指纹编号(1-80)，失败返回0
        if ret != 0:
        #设置指纹灯环为绿色常亮
            fingerprint.ctrl_led(fingerprint.keeps_on, fingerprint.green, 0)
            print("匹配成功,ID = {}".format(ret))
        else:
            print("匹配失败")
    else:
        print("采集失败")
    print("-----------------------------")
    time.sleep(1)
        