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
    "i2c" : {
        "busnum" : [0],
        "class" : "DuinoI2C"
        },
    "spi" : {
        "busnum" : [(0,0)],
        "class" : "DuinoSPI"
        },
    "uart" : {
        "busnum" : [0,1],
        "class" : "DuinoUART",           
        },
    "pin" : {
        "pinnum" : [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19],
        "dpin" : [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19],
        "apin" : [0,1,2,3,4,5],
        "type" : "firmata",
        "class" : "DuinoPin",
        "write_analog" : "firmata"        
        },
    "adc" : {
        "pinadc" : [0,1,2,3,4,5],
        "class" : "DuinoADC",
        "type" : "firmata"
        },
    "pwm" : {
        "pinpwm" : [0,1,2,3,4,5,6,7,8,9,10,11,12,13],
        "class" : "DuinoPWM",
        "type" : "firmata"
        },
    "dht11" : {
        "type" : "firmata",
        "pininvalid" : []
        },
    "dht22" : {
        "type" : "firmata", 
        "pininvalid" : []
        },
    "servo" : {
        "type" : "firmata",
        "class" : "DuinoServo",
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
        "type" : "firmata",
        "pininvalid" : []
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

def get_pin(vpin):
  dpin = vpin if vpin<20 else (vpin-100+14) if vpin >= 100 else -1
  apin = vpin-100 if vpin >= 100 else -1
  if vpin < 100:
    if dpin not in leo_res["pin"]["dpin"]:
      print("不支持数字引脚%d"%vpin)
      return None, None
  else:
    if apin not in uno_res["pin"]["apin"]:
      print("不支持模拟引脚%d"%vpin)
      return None, None
  return dpin,apin

leo_res["init"] = init
leo_res["begin"] = begin
leo_res["reset"] = reset
leo_res["open_serial"] = open_serial
leo_res["find_port"] = find_port
leo_res["soft_reset"] = soft_reset
leo_res["get_pin"] = get_pin

set_globalvar_value("LEONARDO", leo_res)