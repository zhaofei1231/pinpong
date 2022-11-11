# -*- coding: utf-8 -*-
#linux 板通信接口信息


duino_comm_res = {
    
}



Com = {
  
    "_i2c_init" : [False,False,False,False,False], 
    "i2c" : [None, None, None, None, None], 
    "uart" : [None, None, None, None, None], 
    "modbus" : {},
    "_spi_init" : [[False,False], [False,False]],
    "spi" : [[None, None], [None, None]],
    "i2c_fixed" : {"RPI":1,"NEZHA":2,"JH7100":1} 
  }
  
#板子初始化判断信息
 
DuinoBoard = []



#板子烧录信息


#通用linux板

  
inux_board_list = ["RPI", "WIN", "JH7100", "XUGU", "PINPONG"]


#引脚初始化方法
method = {}