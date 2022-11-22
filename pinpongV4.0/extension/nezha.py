# -*- coding: utf-8 -*-

import sys
import platform
import os

from pinpong.extension.globalvar import *
from pinpong.base.comm import *

  
nez_res = {
    "i2c" : {
        "busnum" : [2],
        "class" : " LinuxI2C"
        },
    "spi" : {
        "busnum" : [(0,0),(0,1)],
        "class" : "LinuxSPI"
        },
    "uart" : {
        "busnum" : ["/dev/ttyS3", "/dev/ttyS5"],
        "class" : "TTYUART",           
        },
    "pin" : {
        "pinnum" : [None,33,32,118,40,41,2027,37,   2020,44,2021,2022,108,109,2024,107,    106,2023,110,2025,111,65,38,2026,    35,36],   
        "class" : "SYSFSPin"         
        },
    "pwm" : {
        "pinpwm" : [3,22],
        "class" : "SYSFSPWM",
        "pwmconfig" : {22:{"channel":1, "io":38}, 3:{"channel":7,"io":118}},
        "export_path" : "/sys/class/pwm/pwmchip0/export",
        "comm_path" : "/sys/class/pwm/pwmchip0/pwm"
        },
    "tone" : {       
        "class" : "LinuxTone",
        "pininvalid" : []
        }, 
    "servo" : {        
        "class" : "SYSFSServo",
        "pininvalid" : []
        },
    "dht11" : {
       
        "pininvalid" : []
        },
    "dht22" : {
       
        "pininvalid" : []
        },
    "irrecv" : {
        "class" : "EVENTIRRecv",
        "event" : {20 : "/dev/input/event1"},
        "pininvalid" : []
        }
    }   


def begin(board):
  printlogo_big()
  version = sys.version.split(' ')[0]
  name = platform.platform()
  print("[01] Python"+version+" "+name+(" " if board.boardname == "" else " Board: "+ board.boardname))
  
def init(board, boardname, port):
  board.connected = True
  
  
def reset():
  pass
  
def sofr_reset(board):
  pass
  
def get_pin(board,vpin):
  if vpin ==0 or vpin > len(nez_res["pin"]["pinnum"]):
    raise ValueError("nezha不支持该引脚%d"%vpin, "引脚必须在[%d,%d]",1,len(board.nezha_pinmap)-1)
  board.pinnum = nez_res["pin"]["pinnum"][vpin]
  dpin = apin = vpin
  return dpin,apin

def find_port(board):
  pass

def open_serial(board):
  pass

def PWM(board):

  print(board.io)
  if os.path.exists('/sys/class/gpio/gpio'+board.io):
    os.system('echo '+board.io+' > /sys/class/gpio/unexport')
  if not os.path.exists('/sys/class/pwm/pwmchip0/pwm'+board.channel):
    os.system('echo '+board.channel+' > '+board.export_path)
  board.isStart = False

nez_res["begin"] = begin 
nez_res["init"] = init
nez_res["find_port"] = find_port
nez_res["reset"] = reset
nez_res["sofr_reset"] = sofr_reset
nez_res["get_pin"] = get_pin
nez_res["PWM"] = PWM

set_globalvar_value("NEZHA", nez_res)

  
  

