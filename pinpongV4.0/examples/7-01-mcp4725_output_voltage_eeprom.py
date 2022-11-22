 # -*- coding: utf-8 -*-
import time
from pinpong.board import Board
from pinpong.libs.dfrobot_mcp4725 import MCP4725

Board("uno").begin()#初始化，选择板型和端口号，不输入端口号则进行自动识别
#Board("uno","COM36").begin()  #windows下指定端口初始化
#Board("uno","/dev/ttyACM0").begin()   #linux下指定端口初始化
#Board("uno","/dev/cu.usbmodem14101").begin()   #mac下指定端口初始化

ref_voltage    = 5000
output_voltage = 1000
dac = MCP4725()

#address0 -->0x60
#address1 -->0x61

dac.init(dac.address0, ref_voltage)

while True:
    print("DFRobot_MCP4725 write to EEPROM and output: {} mV".format(output_voltage))
    dac.output_voltage_EEPROM(output_voltage)
    time.sleep(0.2)