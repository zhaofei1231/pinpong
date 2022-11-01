# -*- coding: utf-8 -*-
import serial
import platform
import sys
import time

from pinpong.base import pymata4
from pinpong.extension.globalvar import *
from pinpong.extension.comm import *

uno_res = {}



def begin(board):
  version = sys.version.split(' ')[0]
  name = platform.platform()
  if board.boardname == "PinPong Board":
    print("[01] Python"+version+" "+name+" Board: "+ "PinPong Board")
    uno_res.update["firmware"] = ["/base/FirmataExpress.UNO_PB.", ".hex"]
  else:
    print("[01] Python"+version+" "+name+(" " if board.boardname == "" else " Board: "+ board.boardname))
    if name.find("Linux_vvBoard_OS")>=0 or name.find("Linux-4.4.159-aarch64-with-Ubuntu-16.04-xenial")>=0:
      cmd = "/home/scope/software/avrdude-6.3/avrdude -C/home/scope/software/avrdude-6.3/avrdude.conf -v -patmega328p -carduino -P"+self.port+" -b115200 -D -Uflash:w:"+cwdpath + "/base/FirmataExpress.UNO."+str(FIRMATA_MAJOR)+"."+str(FIRMATA_MINOR)+".hex"+":i"
      os.system(cmd)
    else:
      uno_res["firmware"] = ["/base/FirmataExpress.UNO.", ".hex"]
  
#资源初始化
#打印logo
#  
def init(board, boardname, port):
  if port == 8081:#wifi port
      printlogo_big()
      self.ip = boardname
      self.port = port
      self.boardname = "UNO"
      self.board = pymata4.Pymata4(ip_address=self.ip, ip_port=self.port)
      self.board.i2c_write(0x10, [0,0,0])
      self.board.i2c_write(0x10, [2,0,0])

  name = platform.platform()
  board.connected = False #验证一下是值传递还是引用传递

def soft_reset(board):
  
  pass
  
def reset():
  self.serial = serial.Serial(self.port, 115200, timeout=times[self.boardname])
  
def reset_delay():
  time.sleep(2)

def open_serial(board):
  board.serial = serial.Serial(board.port, 115200, timeout=board.duration[board.boardname])
  time.sleep(2)

uno_res = {
    "i2c" : [0], 
    "uart" : [0],
    "begin" : begin,
    "init" : init,
    "open_serial" : open_serial,
    "pin" : {
        "type" : "general",
        "class" : "DuinoPin",
        "pinnum" : False,
        "pinmap" : []
        },
    "pwm" : {
        "class" : "DuinoPWM",
        "type" : "general"
        },
    "dht11" : "general",
    "dht22" : "dht22"            
    }
uno_res["soft_reset"] = soft_reset
  

set_globalvar_value("UNO", uno_res)
