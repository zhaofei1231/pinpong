# -*- coding: utf-8 -*-
import time
from pinpong.board import Board
from pinpong.libs.dfrobot_max30102 import DFRobot_BloodOxygen_S

Board().begin()

max30102 = DFRobot_BloodOxygen_S()

while (False == max30102.begin()):
    print("init fail!")
    time.sleep(1)
print("start measuring...")
max30102.sensor_start_collect()

while True:
    print("SPO2 is : "+str(max30102.get_spo2())+"%") 
    print("heart rate is : "+str(max30102.get_heartbeat())+"Times/min")
    time.sleep(1)