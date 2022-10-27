# -*- coding: utf-8 -*-

from comm import *

try:
  import RPi.GPIO as GPIO
except Exception:
  pass
  
rpi_res = {
    "pwm":[D1,D2,D3,D4],
    "i2c" : [2],
    "uart" : [1,2],
    "begin":begin,
    "init":init,
    "pin" : {
        type : "general",
        "class" : "RPiPin",
        "pinnum" : True,
        "pinmap" : [P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11,  
         P13, P15, P16, P17, P18, P19, P20, P21, P22, P23, P24, P25,
         P26, P27, P28, P30, P31, P32]
        
        }
    "pwm" : {
        type:"dfrobot",
        "class" : "RpiPWM",
        },
    "tone" : {
        type : "general",
        "class" : "RpiTone"
        } 
    "servo" : {
        type : "general",
        "class" : "RpiServo",
        
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


 
 
 
set_globalvar_value("RPI", rpi_res)

  
  

