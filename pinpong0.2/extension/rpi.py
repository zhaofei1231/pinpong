# -*- coding: utf-8 -*-

from pinpong.extension.comm import *
from pinpong.extension.globalvar import *
from pinpong.base.comm import *

try:
  import RPi.GPIO as GPIO
except Exception:
  pass
  
rpi_res = {
    "i2c" : 1,
    "uart" : {
        "class" : "TTYUART"
        
        },
    "spi" : {
        "class" : "RPiSPI"
        
        },
    "uart" : [1,2],
    "pin" : {
        "type" : "general",
        "class" : "RPiPin",
        "pinnum" : True,
        "analog" : "dfrobot"
        },
    "pwm" : {
        "type" : "dfrobot",
        "class" : "RpiPWM",
        },
    "tone" : {
        "type" : "general",
        "class" : "RpiTone"
        }, 
    "servo" : {
        "type" : "general",
        "class" : "RPiServo",
        },
    "irrecv" : {
        "class" : "EVENTIRRecv"
        }
    }    
gthreads = []


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

def find_port(board):
  pass

rpi_res["begin"] = begin 
rpi_res["init"] = init
uno_res["find_port"] = find_port

set_globalvar_value("RPI", rpi_res)

  
  

