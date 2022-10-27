# -*- coding: utf-8 -*-
#linux 板通信接口信息

def globalcomm_init():
  global Com 
  Com = {
  
    "_i2c_init" : [False,False,False,False,False], 
    "i2c" : [None, None, None, None, None], 
    "uart" : [None, None, None, None, None], 
    "modbus" : {},
    "_spi_init" : [[False,False], [False,False]],
    "spi" : [[None, None], [None, None]],
    "i2c_fixed" : {"RPI":1,"NEZHA":2,"JH7100":1}, 
  
  }
  
#板子初始化判断信息
  global Meg
  Meg = {  
  "boardname" : "",
  "connect" : False,
  "port" : None,
  "spi_wifi_uno" : False
  }

#板子烧录信息
  global firm
  firm = {
      "UNO_PB" : ["/base/FirmataExpress.UNO_PB.", ".hex"],
      "UNO" : ["/base/FirmataExpress.UNO.", ".hex"],
      "LEONARDO" : ["/base/FirmataExpress.LEONARDO.", ".hex"],
      "MEGA2560" : ["/base/FirmataExpress.MEGA2560.", ".hex"],
      "HANDPY" : ["/base/FirmataExpress.HANDPY.", ".bin"],
      "MICROBITV1" : ["/base/FirmataExpress.MICROBIT.", ".hex"],
      "MICROBITV2" : ["/base/FirmataExpress.MICROBITV2.", ".hex"],
      "UNIHIKER" : ["/base/FirmataExpress.UNIHIKER.", ".bin"]
    }
    
#通用linux板

  global linux_board_list
  linux_board_list = ["RPI", "WIN", "JH7100", "XUGU", "PINPONG"]

def set_globalcom(key, num, value):
  Com["key"][num] = value
def set_globalmeg(key, value):
  Meg["key"] = value
def get_globalcom():
  return Com
def get_globalmeg():
  return Meg