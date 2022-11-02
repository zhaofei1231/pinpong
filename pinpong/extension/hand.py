# -*- coding: utf-8 -*- 

import platform
import sys
import serial

from pinpong.extension.globalvar import *
from pinpong.base.comm import *


han_res = {
    "i2c" : None,
    "pin" : {
        "type" : "general",
        "class" : "DuinoPin",
        "pinnum" : True,  
        },
    "pwm" : {
        "class" : "DuinoPWM",
        "type" : "general" 
    },
    "adc" : {
        "type" : "dfrobot",
        "class" : "DuinoADC",
        },
    "tone" : {
        "type" : "dfrobot",
        "class" : "DuinoTone"
        },
    "servo" : {
        "type" : "general",
        "class" : "DuinoServo"
        },
    "dht11" : "dfrobot",
    "dht22" : "dfrobot"    
    }
  
def init(board, boardname, port):
  printlogo()
  board.connected = False
  
def begin(board):
  han_res["firmware"] = ["/base/FirmataExpress.HANDPY.", ".bin"]
  print(han_res["firmware"])
def open_serial(board):
  if sys.platform == "win32":
    board.serial = serial.Serial(board.port, 115200, dsrdtr = True, rtscts =True, timeout=board.duration[board.boardname])
  else:
    board.serial = serial.Serial(board.port, 115200, timeout=board.duration[board.boardname])

def soft_reset(board):
  board.serial.read(board.serial.in_waiting)
  reset_buf=bytearray(b"\xf0\x0d\x55\xf7")
  board.serial.write(reset_buf)
  reset = board.serial.read(1024)

han_res["init"] = init
han_res["begin"] = begin 
han_res["open_serial"] = open_serial
han_res["soft_reset"] = soft_reset

  
set_globalvar_value("HANDPY", han_res)