# -*- coding: utf-8 -*- 
import serial
import platform
import sys
import time
import os

from pinpong.extension.globalvar import *
from pinpong.base.comm import *

uni_res = {
    "i2c" : None, 
    "uart" : {
        "class" : "DuinoUART" 
        },
    "pin" : {
        "type" : "general",
        "class" : "DuinoPin",
        "pinnum" : True,
        "analog" : "dfrobot"
        },
    "adc" : {
        "class" : "DuinoADC",
        "type" : "general"
        },
    "pwm" : {
        "class" : "DuinoPWM",
        "type" : "general"
        },
    "dht11" : "general",
    "dht22" : "dht22", 
    "servo" : {
        "type" : "general",
        "class" : "DuinoServo"
        },
    "irrecv" : {
        "class" : "DuinoIRRecv"
        },
    "irremote" : {
        "class" : "DuinoIRRemote"
        },        
  
    "servo" : {
        "type" : "dfrobot",
        "class" : "DuinoServo"
        },
    "tone" : {
        "type" : "general",
        "class" : "DuinoTone" 
        },
    "sr04" : {
        "type" : "general"
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

uni_res["init"] = init
uni_res["begin"] = begin
uni_res["reset"] = reset
uni_res["open_serial"] = open_serial 
 
 
set_globalvar_value("UNIHIKER", uni_res)