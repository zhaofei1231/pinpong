# -*- coding: utf-8 -*-
import serial
import platform
import sys
import time

from pinpong.base import pymata4
from pinpong.base.comm import *
from pinpong.extension.globalvar import *
from pinpong.extension.comm import *

uno_res = {
    "i2c" : {
        "busnum" : [0,1],
        "class" : "DuinoI2C"
        },
    "spi" : {
        "busnum" : [(0,0)],
        "class" : "DuinoSPI"
        },
    "uart" : {
        "busnum" : [0,1,3],
        "class" : "DuinoUART",           
        },
    "pin" : {
        "pinnum" : [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19],
        "dpin" : [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19],
        "apin" : [2,3,4,5],
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
        "pinpwm" : [2,3,4,5,6,7,8,9,10,11,12,13],  
        "class" : "DuinoPWM",
        "type" : "firmata"
        },
    "tone" : {
        "type" : "firmata",
        "class" : "DuinoTone" ,
        "pininvalid" : []
        },
    "dht11" : {
        "type" : "firmata",
        "pininvalid" : [0,1]
        },
    "dht22" : {
        "type" : "firmata", 
        "pininvalid" : [0,1]
        },
    "servo" : {
        "type" : "firmata",
        "class" : "DuinoServo",
        "pininvalid" : [0,1]
        },
    "irrecv" : {
        "class" : "DuinoIRRecv",
        "pininvalid" : [0,1,4,5,6,7,8,9,10,11,12,13]
        },
    "irremote" : {
        "class" : "DuinoIRRemote",
        "pininvalid" : [0,1]
        },
    "sr04" : {  #两个引脚不做判断
        "type" : "firmata",
        "pininvalid" : []
        }        
    }

def begin(board): 
  printlogo_big()
  version = sys.version.split(' ')[0]
  name = platform.platform()
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
  board.connected = False 

def soft_reset(board):
  pass
  
def reset():
  #self.serial = serial.Serial(self.port, 115200, timeout=times[self.boardname])
  pass
def reset_delay():
  time.sleep(2)

def open_serial(board):
  board.serial = serial.Serial(board.port, 115200, timeout=board.duration[board.boardname])
  time.sleep(2)

def find_port(board):
  pass

def get_pin(vpin):
  dpin = vpin if vpin<20 else (vpin-100+14) if vpin >= 100 else -1
  apin = vpin-100 if vpin >= 100 else -1
  if vpin < 100:
    if dpin not in uno_res["pin"]["dpin"]:
      raise ValueError("UNO不支持该数字引脚%d"%vpin, "支持数字引脚",uno_res["pin"]["dpin"])
     
  else:
    if apin not in uno_res["pin"]["apin"]:
      raise ValueError("UNO不支持该模拟引脚%d"%vpin, "支持模拟引脚",uno_res["pin"]["apin"])

  return dpin,apin
  
uno_res["init"] = init
uno_res["begin"] = begin
uno_res["reset"] = reset
uno_res["soft_reset"] = soft_reset
uno_res["open_serial"] = open_serial
uno_res["find_port"] = find_port
uno_res["get_pin"] = get_pin

set_globalvar_value("UNO", uno_res)
