# -*- coding: utf-8 -*-

import platform
import serial
import time
import sys


from pinpong.base import pymata4
from pinpong.extension.globalvar import *
from pinpong.base.comm import *
from pinpong.base.avrdude import *


leo_res = {
    "i2c" : None, 
    "spi" : {
        "class" : "DuinoSPI"
        
        },
    "uart" : {
        "class" : "DuinoUART" 
        },
    "pin" : {
        "type" : "general",
        "class" : "DuinoPin",
        "pinnum" : False,
        "analog" : "general"
        
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
    "dht22" : "general", 
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
    "flag" : 1,
    "sr04" : {
        "type" : "general"
        }
}


def init(board, boardname, port):
    printlogo()
    name = platform.platform()
    board.connected = False #验证一下是值传递还是引用传递


def begin(board):
    
    leo_res["firmware"] = ["/base/FirmataExpress.LEONARDO.", ".hex"]
    
   

#复位板子
#使用1200波特率打开串口，再用1200波特率关闭串口
def reset():
  #s = serial.Serial(board.port, 1200)
  #s.close()
  time.sleep(1)

def find_port(board):
    port_list_0 = list(serial.tools.list_ports.comports())
    port_list_2 = port_list_0 = [list(x) for x in port_list_0]
    ser = serial.Serial(board.port,1200,timeout=1) #复位
    ser.close()
    time.sleep(0.2)
    retry = 5
    port = None
    while retry:
      retry = retry - 1

      port_list_2 = list(serial.tools.list_ports.comports())
      port_list_2 = [list(x) for x in port_list_2]
      print("port_list_2", port_list_2)
      print("port_list_0", port_list_0)
      for p in port_list_2:
        if p not in port_list_0:
          port = p
          print("port = ", port)
          break
      if port == None:
        time.sleep(0.5)
      if port: #找到了BootLoader串口
        break
    
    if port == None:
      print("[99] can NOT find ",board.boardname)
      sys.exit(0)
    board.pgm = Burner(board.boardname, port[0])

def open_serial(board):
  board.serial = serial.Serial(board.port, 115200, timeout=board.duration[board.boardname])
  
def soft_reset(board):
  pass

leo_res["init"] = init
leo_res["begin"] = begin
leo_res["reset"] = reset
leo_res["open_serial"] = open_serial
leo_res["find_port"] = find_port
leo_res["soft_reset"] = soft_reset
uno_res["find_port"] = find_port

set_globalvar_value("LEONARDO", leo_res)