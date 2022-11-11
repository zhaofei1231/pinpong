# -*- coding: utf-8 -*- 
import serial
import platform
import sys
import time
import os

from pinpong.extension.globalvar import *
from pinpong.base.comm import *

uni_res = {
    "i2c" : {
        "busnum" : [0],
        "class" : "DuinoI2C"
        },
    "spi" : {
        "busnum" : [(0,0)],
        "class" : "DuinoSPI"
        },
    "uart" : {
        "busnum" : [0],
        "class" : "DuinoUART",           
        },
    "pin" : {
        "pinnum" : [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,19,20,21,22,23,24,25,26],
        "dpin" :[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,19,20,21,22,23,24,25,26],
        "apin" : [0,1,2,3,4,10],
        "type" : "firmata",
        "class" : "DuinoPin",
        "write_analog" : "dfrobot_firmata"        
        }, 
    "adc" : {
        "pinadc" : [0,1,2,3,4,10,21,22],
        "class" : "DuinoADC",
        "type" : "firmata"
        },
    "pwm" : {
        "pinpwm" : [0,2,3,8,9,10,16,21,22,23,5],
        "class" : "DuinoPWM",
        "type" : "dfrobot_firmata"
        },
    "dht11" : {
        "type" : "firmata",
        "pininvalid" : [13]
        },
    "dht22" : {
        "type" : "firmata", 
        "pininvalid" : [13]
        },
    "servo" : {
        "type" : "firmata",
        "class" : "DuinoServo",
        "pininvalid" : [1,4,5,6,7,11,12,13,14,15,16,19,20,21,22,23,24]
        },
    "irrecv" : {
        "class" : "DuinoIRRecv",
        "pininvalid" : [11,13]
        },
    "irremote" : {
        "class" : "DuinoIRRemote",
        "pininvalid" : [5,6,7,13]
        },        
    "tone" : {
        "type" : "firmata",
        "class" : "DuinoTone" ,
        "pininvalid" : []
        },
    "sr04" : {
        "type" : "firmata",
        "pininvalid" : []
        }
  }

def init(board, boardname, port):
  printlogo()
  board.connected = False
  
def begin(board):
  uni_res["firmware"] = ["/base/FirmataExpress.UNIHIKER.", ".bin"]
  board.port = "/dev/ttyS3"


def reset():
  if not os.path.exists("/sys/class/gpio/gpio80"):
    os.system("echo 80 > /sys/class/gpio/export")#RST
  if not os.path.exists("/sys/class/gpio/gpio69"):
   os.system("echo 69 > /sys/class/gpio/export")#BOOT0      
  os.system("echo out > /sys/class/gpio/gpio69/direction")
  os.system("echo out > /sys/class/gpio/gpio80/direction")
  os.system("echo 0 > /sys/class/gpio/gpio69/value")
  os.system("echo 1 > /sys/class/gpio/gpio80/value")
  os.system("echo 0 > /sys/class/gpio/gpio80/value")
  os.system("echo 1 > /sys/class/gpio/gpio80/value")
 
def open_serial(board):
  board.serial = serial.Serial(board.port, 115200, timeout=board.duration[board.boardname])

def find_port(board):
  pass

def get_pin(vpin):
  if vpin not in uni_res["pin"]["pinnum"]:
    print("不支持该引脚%d"%vpin)
    return None, None
  dpin = apin = vpin
  return dpin,apin

def soft_reset(board):
  pass
uni_res["init"] = init
uni_res["begin"] = begin
uni_res["reset"] = reset
uni_res["open_serial"] = open_serial 
uni_res["find_port"] = find_port 
uni_res["get_pin"] = get_pin
uni_res["soft_reset"] = soft_reset 
set_globalvar_value("UNIHIKER", uni_res)