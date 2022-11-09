# -*- coding: utf-8 -*- 

import platform
import sys
import serial

from pinpong.extension.globalvar import *
from pinpong.base.comm import *


han_res = {
    "i2c" : {
        "num" : [0],
        "class" : "DuinoI2C"
        },
    "spi" : {
        "num" : [(0,0)],
        "class" : "DuinoSPI"
        },
    "uart" : {
        "num" : [0],
        "class" : "DuinoUART",           
        },
    "pin" : {
        "pinnum" : [0,1,2,3,4,5,6,7,8,9,10,11,13,14,15,16,19,20],
        "dpin" :[0,1,2,5,6,7,8,9,13,14,15,16,19,20],
        "apin" : [0,1,2,3,4,10],
        "type" : "",
        "write_analog" : "dfrobot_firmata"         
        }, 
    "pwm" : {
        "pinpwm" : [0,1,5,6,7,8,9,11,13,14,15,16],
        "type" : "dfrobot_firmata",
        "class" : "DuinoPWM"       
    },
    "adc" : {
        "pinadc" : [0,1,2,3,4,10],
        "type" : "dfrobot_firmata",
        "class" : "DuinoADC",
        },
    "tone" : {
        "type" : "dfrobot_firmata",
        "class" : "DuinoTone",
        "pininvalid" : []
        },
    "servo" : {
        "type" : "firmata",
        "class" : "DuinoServo",
        "pininvalid" : []
        },
    "dht11" : {
        "type" : "firmata",
        "pininvalid" : []
        },
    "dht22" : {
        "type" : "firmata", 
        "pininvalid" : []
        },
    "irrecv" : {
        "class" : "DuinoIRRecv",
        "pininvalid" : []
        },
    "irremote" : {
        "class" : "DuinoIRRemote",
        "pininvalid" : []
        },
    "sr04" : {
        "type" : "dfrobot_firmata",
        "pininvalid" : []
        }        
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

def reset():
  pass

def soft_reset(board):
  board.serial.read(board.serial.in_waiting)
  reset_buf=bytearray(b"\xf0\x0d\x55\xf7")
  board.serial.write(reset_buf)
  reset = board.serial.read(1024)
  
def find_port(board):
  pass

def get_pin(vpin):
  if vpin not in han_res["pinnum"]:
    print("不支持该引脚%d"%vpin)
    return None, None
  dpin = apin = vpin
  return dpin,apin

han_res["init"] = init
han_res["begin"] = begin 
han_res["open_serial"] = open_serial
han_res["soft_reset"] = soft_reset
han_res["reset"] = reset
han_res["find_port"] = find_port
han_res["get_pin"] = get_pin

set_globalvar_value("HANDPY", han_res)