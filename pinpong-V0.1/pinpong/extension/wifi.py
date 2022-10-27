# -*- coding: utf-8 -*- 

def wifibegin(ip, port):
  board = pymata4.Pymata4(ip, port)
  board.i2c_write(0x10, [0,0,0])
  board.i2c_write(0x10, [2,0,0])
 
  
  
  
