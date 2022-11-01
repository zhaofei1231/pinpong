# -*- coding: utf-8 -*-

from comm import *

try:
  import RPi.GPIO as GPIO
except Exception:
  pass
  
rpi_res = {
    "i2c" : [2],
    "uart" : [1,2],
    "begin":begin,
    "init":init,
    "pin" : {
        "type" : "general",
        "class" : "RPiPin",
        "pinnum" : True,
        "pinmap" : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 
         13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
         26, 27, 28, 29, 30, 31, 32]
        
        }
    "pwm" : {
        "type" : "dfrobot",
        "class" : "RpiPWM",
        },
    "tone" : {
        "type" : "general",
        "class" : "RpiTone"
        } 
    "servo" : {
        "type" : "general",
        "class" : "RpiServo",
        },
    "irrecv" : {
        "class" : "EVENTIRRecv"
        },
    "irremote" : {
        
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

  
  

