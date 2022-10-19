# -*- coding: utf-8 -*-

#实验效果：引脚模拟中断功能测试
#接线：使用windows或linux电脑连接一块arduino主控板，主控板D8接一个按钮模块
import time
from pinpong.board import Board,Pin

Board("xugu").begin()

btn = Pin(Pin.D8, Pin.IN)

def btn_rasing_handler(pin):#中断事件回调函数
  print("\n--rising---")
  print("pin = ", pin)
  
def btn_falling_handler(pin):#中断事件回调函数
  print("\n--falling---")
  print("pin = ", pin)

def btn_both_handler(pin):#中断事件回调函数
  print("\n--both---")
  print("pin = ", pin)

btn.irq(trigger=Pin.IRQ_FALLING, handler=btn_falling_handler) #设置中断模式为下降沿触发
#btn.irq(trigger=Pin.IRQ_RISING, handler=btn_rasing_handler) #设置中断模式为上升沿触发，及回调函数
#btn.irq(trigger=Pin.IRQ_RISING+Pin.IRQ_FALLING, handler=btn_both_handler) #设置中断模式为电平变化时触发

while True:
  time.sleep(1)
