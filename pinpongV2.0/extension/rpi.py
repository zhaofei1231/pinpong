# -*- coding: utf-8 -*-

from pinpong.extension.comm import *
from pinpong.extension.globalvar import *
from pinpong.base.comm import *

try:
  import RPi.GPIO as GPIO
except Exception:
  pass
  
rpi_res = {
    "i2c" : {
        "busnum" : [0,1],
        "class" : "RPiI2C"
        },
    "spi" : {
        "busnum" : [(0,0)],
        "class" : "RPiSPI"
        },
    "uart" : {
        "busnum" : [0],
        "class" : "TTYUART",           
        },
    "pin" : {
        "pinnum" : [4,5,6,12,13,16,17,18,19,20,21,22,23,24,25,26,27],
        "dpin" : [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,
        18,19,20,21,22,23,24,25,26,27],      
        "class" : "RPiPin",
        "write_analog" : "dfrobot_firmata"         
        },
    "pwm" : {
        "class" : "RpiPWM",
        "pininvalid" : [4,5,6,12,13,16,17,18,19,20,21,22,23,24,25,26,27]
        },
    "tone" : {       
        "class" : "RpiTone",
        "pininvalid" : [4,5,6,12,13,16,17,18,19,20,21,22,23,24,25,26,27]
        }, 
    "servo" : {
        
        "class" : "RPiServo",
        "pininvalid" : [4,5,6,12,13,16,17,18,19,20,21,22,23,24,25,26,27]
        },
    "dht11" : {
       
        "pininvalid" : [4,5,6,12,13,16,17,18,19,20,21,22,23,24,25,26,27]
        },
    "dht22" : {
       
        "pininvalid" : [4,5,6,12,13,16,17,18,19,20,21,22,23,24,25,26,27]
        },
    "irrecv" : {
        "class" : "EVENTIRRecv",
        "pininvalid" : [4,5,6,12,13,16,17,18,19,20,21,22,23,24,25,26,27]
        }
    }   


def begin(board):
  version = sys.version.split(' ')[0]
  plat = platform.platform()
  print("[01] Python"+version+" "+plat+(" " if board.boardname == "" else " Board: "+ board.boardname))
  

#资源初始化
#打印logo
#  
def init(board, boardname, port):
  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings(False)
  board.connected = True
  printlogo()

def reset():
  pass
  
def sofr_reset(board):
  pass
  
def get_pin(vpin):
  if vpin not in rpi_res["pin"]["pinnum"]:
    raise ValueError("树莓派不支持该引脚%d"%vpin, "支持引脚",rpi_res["pin"]["pinnum"])
    return None, None
  dpin = apin = vpin
  return dpin,apin

def find_port(board):
  pass

def open_serial(board):
  pass

rpi_res["begin"] = begin 
rpi_res["init"] = init
rpi_res["find_port"] = find_port
rpi_res["reset"] = reset
rpi_res["sofr_reset"] = sofr_reset
rpi_res["get_pin"] = get_pin



set_globalvar_value("RPI", rpi_res)

  
  

