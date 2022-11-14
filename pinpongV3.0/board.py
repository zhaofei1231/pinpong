# -*- coding: utf-8 -*-

import os
import sys, getopt
import json
import time
import ctypes
import serial
import signal
import platform
import serial.tools.list_ports
import subprocess
import threading

from pinpong.base.avrdude import *
from pinpong.base import pymata4
from pinpong.base.comm import *
from pinpong.base.i2c import *

from pinpong.extension.globalvar import *
from pinpong.extension.firmata_extension import *


try:
  import smbus
except Exception:
  pass

try:
  import spidev
except Exception:
  pass

try:
  import modbus_tk
  from modbus_tk import modbus_tcp
  from modbus_tk import modbus_rtu
  import modbus_tk.defines as cst
except Exception:
  pass

try:
  import RPi.GPIO as GPIO
except Exception:
  pass

gboard = None
gthreads = []
globalvar_init()


import pinpong.extension.uno
import pinpong.extension.leonardo
import pinpong.extension.rpi
import pinpong.extension.micro
import pinpong.extension.hand
import pinpong.extension.leonardo
import pinpong.extension.unihi


class DuinoPin:
  def __init__(self, board=None, pin=None, mode=None):
    
    self.mode = mode
    self.board = board
    self.pin, self.apin = board.res["get_pin"](pin)
    print("DuinoPin", self.pin, self.apin)
    if(mode == Pin.OUT):
      self.board.board.set_pin_mode_digital_output(self.pin)
    elif(mode == Pin.IN):
      self.board.board.set_pin_mode_digital_input(self.pin, callback=None)
    elif(mode == Pin.PWM):#为了支持面向过程的4个API而设计的此选项，尽量避免使用,使用PWM类代替
      self.board.board.set_pin_mode_pwm_output(self.pin)
    elif(mode == Pin.ANALOG):#为了支持面向过程的4个API而设计的此选项，尽量避免使用，使用ADC类代替
      if board.res["pin"]["type"] == "dfrobot_firmata":     #判断使用哪条pymata命令
        self.board.board.set_pin_analog_input(self.apin, None)
      else:
        self.board.board.set_pin_mode_analog_input(self.apin, None)

  def value(self, v = None):
    if v == None:  #Read
      if self.mode == Pin.OUT:   #*****添加错误信息？*****
        return self.val
      else:
        if self.pin == None:   #*****添加错误信息？*****
          return
        self.val = self.board.board.digital_read(self.pin) 
        return self.val
    else:  #Write
      self.val = v
      if(self.pin == None):
        return
      self.board.board.digital_pin_write(self.pin, v) 
      time.sleep(0.001)

  def on(self):
    self.val = 1
    if self.pin == None:
      return
    self.board.board.digital_pin_write(self.pin, 1)

  def off(self):
    self.val = 0
    if(self.pin == None):
      return
    self.board.board.digital_pin_write(self.pin, 0)

  def irq(self, trigger, handler):
    self.board.board.set_pin_mode_digital_input(self.pin, None)
    self.board.board.set_digital_pin_params(self.pin, trigger, handler) 
  
  #这5个函数将打破原有的面向对象规则，请慎用
  #建议使用value方法 PWM和ADC类来替代这5个函数 
  def write_analog(self, duty):
    self.duty=duty
    self.freq=100
    if self.board.res["pin"]["write_analog"] == "firmata":
      real_duty = int(self.duty / 255 * 100)
      real_duty = 255 if real_duty>255 else real_duty
      self.board.board.pwm_write(self.pin, self.freq, real_duty)
    else:
      self.board.board.dfrobot_pwm_write(self.pin, self.freq, self.duty)

  def write_digital(self, value):
    self.val = value
    if(self.pin == None):
      return
    self.board.board.digital_pin_write(self.pin, value)

  def read_digital(self):
    if(self.pin == None):
      return
    self.val = self.board.board.digital_read(self.pin)
    return self.val

  def read_analog(self):
    return self.board.board.analog_read(self.apin)

  def pin_mode(self, mode):
    if(mode == Pin.OUT):
      self.board.board.set_pin_mode_digital_output(self.pin)
    elif(mode == Pin.IN):
      self.board.board.set_pin_mode_digital_input(self.pin, callback=None)

class RPiPin:
  def __init__(self, board=None, pin=None, mode=None):
    self.board = board
    if(pin == None):
      self.pin = None
      return

    self.pin = pin
    self.mode = mode
    if(mode == Pin.OUT):
      GPIO.setup(self.pin, GPIO.OUT)
    elif(mode == Pin.IN):
      GPIO.setup(self.pin, GPIO.IN)
    elif(mode == Pin.PWM):#为了支持面向过程的4个API而设计的此选项，尽量避免使用,使用PWM类代替
      GPIO.setup(self.pin, GPIO.OUT)
      self.pwm=GPIO.PWM(self.pin, 1000)
      
  def value(self, v = None):
    if v == None:  #Read
      if self.mode == Pin.OUT:
        return self.val
      else:
        if self.pin == None:
          return
        self.val = GPIO.input(self.pin)
        return self.val
    else:  #Write
      self.val = v
      if(self.pin == None):
        return
      GPIO.output(self.pin,v)

  def on(self):
    self.val = 1
    if self.pin == None:
      return
    GPIO.output(self.pin, GPIO.HIGH)

  def off(self):
    self.val = 0
    if(self.pin == None):
      return
    GPIO.output(self.pin, GPIO.LOW)

  def irq(self, trigger, handler):
    OFFSET = 30                                   #30是偏移量
    GPIO.add_event_detect(self.pin, OFFSET+trigger)
    GPIO.add_event_callback(self.pin, handler)
    #GPIO.add_event_detect(self.pin, 30+trigger, callback=handler)
  
  #这5个函数将打破原有的面向对象规则，请慎用
  #建议使用value方法 PWM和ADC类来替代这5个函数 
  def write_analog(self, duty):
    self.duty=duty
    self.pwm.start(duty)

  def write_digital(self, value):
    self.val = value
    if(self.pin == None):
      return
    GPIO.output(self.pin, value)

  def read_digital(self):
    if(self.pin == None):
      return
    self.val = GPIO.input(self.pin)
    return self.val

  def pin_mode(self, mode):
    if(mode == Pin.OUT):
      GPIO.setup(self.pin, GPIO.OUT)
    elif(mode == Pin.IN):
      GPIO.setup(self.pin, GPIO.IN)

class SYSFSPin:
  def __init__(self, board=None, pin=None, mode=None):
    self.board = board
    if(pin == None):
      self.pin = None
      return                  
    self.pin = pin
    self.mode = mode
    self.export_path = '/sys/class/gpio/export'
    self.value_path = '/sys/class/gpio/gpio'+str(self.pin)+'/value'
    self.direction_path = '/sys/class/gpio/gpio'+str(self.pin)+'/direction'
    if not os.path.exists('/sys/class/gpio/gpio'+str(self.pin)):
      os.system('echo '+str(self.pin)+' > '+self.export_path)
    if(mode == Pin.OUT):
      os.system('echo out > ' + self.direction_path)
    elif(mode == Pin.IN):
      os.system('echo in > ' + self.direction_path)
      
  def value(self, v = None):
    if v is None:  #Read
      if self.mode == Pin.OUT:
        return self.val
      else:
        if self.pin is None:
          return
        with open(self.value_path) as f:
          self.val = int(f.read())  
        return self.val
    else:  #Write
      self.val = v
      if(self.pin == None):
        return
      os.system("echo "+str(v)+" > " + self.value_path)

  def on(self):
    self.val = 1
    if self.pin is None:
      return
    os.system("echo 1 > " + self.value_path)

  def off(self):
    self.val = 0
    if(self.pin == None):
      return
    os.system("echo 0 > " + self.value_path)

  def irq(self, trigger, handler):
    pass
    #GPIO.add_event_detect(self.pin, 30+trigger)
    #GPIO.add_event_callback(self.pin, handler)
    #GPIO.add_event_detect(self.pin, 30+trigger, callback=handler)
  #这5个函数将打破原有的面向对象规则，请慎用
  #建议使用value方法 PWM和ADC类来替代这5个函数 
  def write_analog(self, duty):
    self.duty=duty
    self.pwm.start(duty)

  def write_digital(self, val):
    self.val = val
    if(self.pin == None):
      return
    self.value(val)

  def read_digital(self):
    if(self.pin == None):
      return
    if self.mode == Pin.OUT:
        return self.val
    else:
      if self.pin is None:
        return
      with open(self.value_path) as f:
        self.val = int(f.read())  
      return self.val

  def pin_mode(self, mode):
    if(mode == Pin.OUT):
      os.system('echo out > ' + self.direction_path)
    elif(mode == Pin.IN):
      os.system('echo in > ' + self.direction_path)

class Pin:
  D0 = 0
  D1 = 1
  D2 = 2
  D3 = 3
  D4 = 4
  D5 = 5
  D6 = 6
  D7 = 7
  D8 = 8
  D9 = 9
  D10 = 10
  D11 = 11
  D12 = 12
  D13 = 13
  D14 = 14
  D15 = 15
  D16 = 16
  D17 = 17
  D18 = 18
  D19 = 19
  D20 = 20
  D21 = 21
  D22 = 22
  D23 = 23
  D24 = 24
  D25 = 25
  D26 = 26
  D27 = 27
  D28 = 28
  D29 = 29
  D30 = 30
  D31 = 31
  D32 = 32
  D33 = 33
  D34 = 34
  D35 = 35
  D36 = 36
  D37 = 37
  D38 = 38
  D39 = 39
  D40 = 40
  D41 = 41
  D42 = 42
  D43 = 43
  D44 = 44
  D45 = 45
  D46 = 46
  D47 = 47
  D48 = 48
  D49 = 49
  D50 = 50
  D51 = 51
  D52 = 52
  
  A0 = 100
  A1 = 101
  A2 = 102
  A3 = 103
  A4 = 104
  A5 = 105
  A6 = 106
  A7 = 107

  P0 = 0
  P1 = 1
  P2 = 2
  P3 = 3
  P4 = 4
  P5 = 5
  P6 = 6
  P7 = 7
  P8 = 8
  P9 = 9
  P10 = 10
  P11 = 11
  P12 = 12
  P13 = 13
  P14 = 14
  P15 = 15
  P16 = 16
  P17 = 17
  P18 = 18
  P19 = 19
  P20 = 20
  P21 = 21
  P22 = 22
  P23 = 23
  P24 = 24
  P25 = 25   #Pythonboard L灯
  P26 = 26   #Pythonboard 板载蜂鸣器
  P27 = 27   #Pythonboard key_a
  P28 = 28   #Pythonboard key_b
  P29 = 29
  P30 = 30
  P31 = 31
  P32 = 32
  
  OUT = 0
  IN = 1
  IRQ_FALLING = 2
  IRQ_RISING = 1
  IRQ_DRAIN = 7
  PULL_DOWN = 1
  PULL_UP = 2
  PWM     = 0x10
  ANALOG  = 0x11

  def __init__(self, board=None, pin=None, mode=None):
    if isinstance(board, int):#兼容面向过程的4个api
      mode = pin                  #***pin为什么传给mode
      pin = board
      board = gboard
    if board == None:
      board = gboard
        
    self.board = board
    if(pin == None):
      return
    self.pin = pin
    self.mode = mode
    self.pin, self.apin = board.res["get_pin"](pin)
    self.obj = eval(board.res["pin"]["class"]+"(board, pin, mode)") #根据板子对象直接调用对应的pin方法
   
  def value(self, v = None):
    if v == None:  #Read                      
      return self.obj.value(v)
    else:  #Write
      self.obj.value(v)
      time.sleep(0.001)

  def on(self):
    self.val = 1
    if self.pin == None:
      return
    self.obj.on()

  def off(self):
    self.val = 0
    if self.pin == None:
      return
    self.obj.off()

  def irq(self, trigger, handler):
    self.obj.irq(trigger, handler)

  #这5个函数将打破原有的面向对象规则，请慎用
  #建议使用value方法 PWM和ADC类来替代这5个函数
  def write_analog(self, duty):
    self.obj.write_analog(duty)

  def write_digital(self, value):
    self.obj.write_digital(value)

  def read_digital(self):
    return self.obj.read_digital()

  def read_analog(self):
    return self.obj.read_analog()

  def pin_mode(self, mode):
    self.obj.pin_mode(mode)

class DuinoADC:
  def __init__(self, board=None, pin_obj=None):
    if isinstance(board, Pin):
      pin_obj = board
      board = gboard
    elif board == None:
      board = gboard
    
    self.board = board
    self.pin_obj = pin_obj
    
    #print("模拟引脚", self.pin_obj.apin)
    #MICROBIT HANDPY 使用协议 F0 xx(PIN) 02 DF私有Firamata协议
    #UNO使用标准的Firmata协议
    #if board.boardname in ["HANDPY", "MICROBIT"]:
    if board.res["adc"]["type"] == "dfrobot_firmata":     
      self.board.board.set_pin_analog_input(self.pin_obj.apin, None)
    else:
      self.board.board.set_pin_mode_analog_input(self.pin_obj.apin, None)

  def read(self):
    return self.board.board.analog_read(self.pin_obj.apin)
    
class ADC:
  def __init__(self, board=None, pin_obj=None):
    if isinstance(board, Pin):
      pin_obj = board
      board = gboard
    elif board == None:
      board = gboard
    if pin_obj.pin not in board.res["adc"]["pinadc"]:
      raise ValueError("adc不支持该引脚%d"%pin_obj.pin, "支持引脚", board.res["adc"]["pinadc"])
    self.board = board
    self.pin_obj = pin_obj
    self.obj = eval(self.board.res["adc"]["class"]+"(board, pin_obj)")
    
  def read(self):
    return self.obj.read()
    
class DuinoPWM:
  def __init__(self, board, pin_obj):
    self.board = board
    self.pin_obj = pin_obj
    self.freq_value = 100
    self.duty_value = 50
    
    
    self.board.board.set_pin_mode_pwm_output(self.pin_obj.pin)

  def freq(self, v=None):
    if v == None:
      return self.freq_value
    else:
      self.freq_value = v
    #f4（设置引脚模式） 04（引脚） 03（设置引脚模式为PWM模式）
    #e4（设置4号引脚的信息） 10（占空比：16%） 01（频率7~9位） 7f（频率0~6位） 
    if self.board.res["pwm"]["type"] == "firmata":   #更改固件
      real_duty = int(self.duty_value / 255 * 100)
      real_duty = 255 if real_duty>255 else real_duty
      self.board.board.pwm_write(self.pin_obj.pin, self.freq_value, real_duty)
    else:
      self.board.board.dfrobot_pwm_write(self.pin_obj.pin, self.freq_value, self.duty_value)

  def duty(self, v=None):
    if v == None:
      return self.duty_value
    else:
      self.duty_value = v
    if self.board.res["pwm"]["type"] == "firmata":
      real_duty = int(self.duty_value / 255 * 100)
      real_duty = 255 if real_duty>255 else real_duty
      self.board.board.pwm_write(self.pin_obj.pin, self.freq_value, real_duty)
    else:
      self.board.board.dfrobot_pwm_write(self.pin_obj.pin, self.freq_value, self.duty_value)

  def deinit(self):
    self.board.pin_obj.pin_mode(Pin.IN)

class RpiPWM:
  def __init__(self, board, pin_obj):
    self.pin_obj = pin_obj
    self.freq_value = 100
    self.duty_value = 50
    GPIO.setup(self.pin_obj.pin, GPIO.OUT)
    self.pwm = GPIO.PWM(self.pin_obj.pin, self.freq_value)
    #self.pwm.start(duty)
    self.isStart = False

  def freq(self, v=None):
    if v == None:
      return self.freq_value
    else:
      self.freq_value = v
      if v == 0:
        self.pwm.stop()
        self.isStart = False
      else:
        self.pwm.start(self.duty_value)
        self.pwm.ChangeFrequency(self.freq_value)
        self.isStart = True

  def duty(self, v=None):
    if v == None:
      return self.duty_value
    else:
      self.duty_value = v
    self.pwm.ChangeDutyCycle(self.duty_value)

  def deinit(self):
    self.pwm.stop()

class SYSFSPWM:
  def __init__(self, board, pin_obj):
    self.pin_obj = pin_obj
    
    self.period_ns = 10000000
    if self.pin_obj.pin not in [7]:#PWM0-GPIO7
      raise ValueError("invalid pin ",self.pin_obj.pin)
    self.pwms={7:{"channel":0, "io":38}}
    self.io = str(self.pwms[self.pin_obj.pin]["io"])
    self.channel = str(self.pwms[self.pin_obj.pin]["channel"])
    self.export_path = '/sys/class/pwm/pwmchip0/export'
    self.period_path = '/sys/class/pwm/pwmchip0/pwm'+self.channel+'/period'
    self.duty_path = '/sys/class/pwm/pwmchip0/pwm'+self.channel+'/duty_cycle'
    self.enable_path = '/sys/class/pwm/pwmchip0/pwm'+self.channel+'/enable'

    if len(board.res["pwm"]["GPIO"]) > 1:
      if os.path.exists('/sys/class/gpio/gpio'+self.io):
      #print('echo '+self.io+' > /sys/class/gpio/unexport')
        os.system('echo '+self.io+' > /sys/class/gpio/unexport')
    if not os.path.exists('/sys/class/pwm/pwmchip0/pwm'+self.channel):
      #print('echo '+self.channel+' > '+self.export_path)
      os.system('echo '+self.channel+' > '+self.export_path)
    self.isStart = False

  def freq(self, v=None):
    if v == None:
      return self.freq_value
    else:
      if v == 0:
        #print('echo 0 > /sys/class/pwm/pwmchip0/pwm'+self.channel+'/enable')
        os.system('echo 0 > /sys/class/pwm/pwmchip0/pwm'+self.channel+'/enable')
        self.isStart = False
        return
      self.freq_value = v
      self.period_ns = int(1000000000/self.freq_value)
      #print('echo '+str(self.period_ns)+' > /sys/class/pwm/pwmchip0/pwm'+self.channel+'/period')
      os.system('echo '+str(self.period_ns)+' > /sys/class/pwm/pwmchip0/pwm'+self.channel+'/period')

      if self.isStart == False:
        #print('echo 1 > /sys/class/pwm/pwmchip0/pwm'+self.channel+'/enable')
        os.system('echo 1 > /sys/class/pwm/pwmchip0/pwm'+self.channel+'/enable')
        self.isStart = True

  def duty(self, v=None):
    if v == None:
      return self.duty_value
    else:
      self.duty_value = v
      duty_ns = int(self.period_ns*(100-self.duty_value)/100.0)
      #print('echo '+str(duty_ns)+' > '+self.duty_path)
      os.system('echo '+str(duty_ns)+' > '+self.duty_path)
      if self.isStart == False:
        #print('echo 1 > /sys/class/pwm/pwmchip0/pwm'+self.channel+'/enable')
        os.system('echo 1 > /sys/class/pwm/pwmchip0/pwm'+self.channel+'/enable')
        self.isStart = True

  def deinit(self):
    os.system('echo 0 > /sys/class/pwm/pwmchip0/pwm'+self.channel+'/enable')
    self.isStart = False

class PWM:
  def __init__(self, board=None, pin_obj=None):
    if isinstance(board, Pin):
      pin_obj = board
      board = gboard
    elif board == None:
      board = gboard

    self.board = board
    self.pin_obj = pin_obj
    if pin_obj.pin not in board.res["pwm"]["pinpwm"]:
      raise ValueError("pwm不支持该引脚%d"%pin_obj.pin, board.res["pwm"]["pinpwm"])
    self.freq_value = 100
    self.duty_value = 50

    self.obj = eval(board.res["pwm"]["class"]+"(board, pin_obj)")

  def freq(self, v=None):
    if v == None:
      return self.freq_value
    else:
      self.freq_value = v
      
    if v == None:
      return self.obj.freq(v)
    else:
      self.obj.freq(v)

  def duty(self, v=None):
    if v == None:
      return self.duty_value
    else:
      self.duty_value = v
    
    if v == None:                                       #***有什么区别
      return self.obj.duty(v)
    else:
      self.obj.duty(v)

  def deinit(self):
    self.obj.deinit()
  

class DuinoSPI:
  def __init__(self, board, device_num, cs, bus_num = 0, baudrate=10000):
    self.board = board
    self.device_num = device_num
    self.board.board.set_pin_mode_spi(device_num, cs)

  def read(self, length, default_value=0xff):
    ret = self.board.board.spi_read(self.device_num, length)
    return ret

  def readinto(self, buf):
    length = len(buf)
    buf=self.board.spi_read(self.device_num, length)

  def write(self, buf): #write some bytes on MOSI
    if isinstance(buf, list):
      self.board.board.spi_write(self.device_num, buf)
    else:
      self.board.board.spi_write(self.device_num, [buf])

  def write_readinto(self, wbuf, rbuf): # write to MOSI and read from MISO into the buffer
    rbuf=self.board.board.xfer3(wbuf)

class SoftSPI:
  def __init__(self, board, sck, mosi, miso, baudrate=100000, polarity=0, phase=0, bits=8):
    self.board = board
    self.mosi = mosi
    self.miso = miso
    self.sck = sck
    self.phase = phase
    self.mosi.value(0)
    self.sck.value(polarity)

  def read(self, num, default_value=0xff):
    ret = bytearray(num)
    for i in range (num):
      ret[i] = self._transfer(default_value)
    return ret

  def readinto(self, buf):
    num = len(buf)
    buf=self.read(num)

  def write(self, buf): #write some bytes on MOSI
    num = len(buf)
    for i in range (num):
      self._transfer(buf[i])

  def write_readinto(self, wbuf, rbuf): # write to MOSI and read from MISO into the buffer
    num = len(wbuf)
    for i in range (num):
      rbuf[i] = self._transfer(wbuf[i])

  def _transfer(self,data):
    ret = 0
    for i in range(8):
      self.mosi.value(1 if data&0x80 else 0)
      self.sck.value(0 if self.sck.value() else 1) #这样书写兼容了MODE0 和 MODE3
      self.sck.value(0 if self.sck.value() else 1)
      if self.miso:
        ret= ret<<1 + self.miso.value()
      data <<= 1
    return ret

class RPiSPI:
  def __init__(self, bus_num=0, device_num=0, baudrate=31200000):
    self.spi = spidev.SpiDev(bus_num, device_num)
    self.spi.open(bus_num, device_num)
    self.spi.max_speed_hz = baudrate

  def read(self, num, default_value=0xff):
    ret = self.spi.readbytes(num)
    return ret

  def readinto(self, buf):
    num = len(buf)
    buf=self.read(num)

  def write(self, buf): #write some bytes on MOSI
    self.spi.xfer3(buf)

  def write_readinto(self, wbuf, rbuf): # write to MOSI and read from MISO into the buffer
    num = len(wbuf)

class SPI:
  # spi四种模式SPI的相位(CPHA)和极性(CPOL)分别可以为0或1，对应的4种组合构成了SPI的4种模式(mode)
  # Mode 0 CPOL=0, CPHA=0  ->  第一个跳变，即上升沿采样
  # Mode 1 CPOL=0, CPHA=1  ->  第二个跳变，即下降沿采样
  # Mode 2 CPOL=1, CPHA=0  ->  第一个跳变，即下降沿采样
  # Mode 3 CPOL=1, CPHA=1  ->  第二个跳变，即上升沿采样
  # 时钟极性CPOL: 即SPI空闲时，时钟信号SCLK的电平 (1:空闲时高电平; 0:空闲时低电平)
  # 时钟相位CPHA: 即SPI在SCLK第几个边沿开始采样 (0:第一个边沿开始; 1:第二个边沿开始)
  # 默认设置为MODE 0 因为大部分的外设使用的是MODE 0
  def __init__(self, board=None, bus_num=0, device_num=0, sck=None, mosi=None, miso=None, cs=None, baudrate=100000, polarity=0, phase=0, bits=8):
    if isinstance(board, int):
      device_num = board
      bus_num = device_num
      board = gboard
    elif board == None:
      board = gboard
    self.board = board
    self.board.spi[bus_num][device_num] = eval(self.board.res["spi"]["class"]+"(bus_num, device_num)")
    if self.board.spi not in board.res["spi"]["busnum"]:
      raise ValueError("spi不支持该设备", self.board.spi, "支持",self.board.res["spi"]["bus_num"])
    self.obj = self.board.spi[bus_num][device_num]

  def read(self, num, default_value=0xff):
    return self.obj.read(num, default_value)

  def readinto(self, buf):
    self.obj.readinto(buf)

  def write(self, buf): #write some bytes on MOSI
    self.obj.write(buf)

  def write_readinto(self, wbuf, rbuf): # write to MOSI and read from MISO into the buffer
    self.obj.writeinto(wbuf, rbuf)

class DuinoI2C:
  def __init__(self, board, bus_num):
    self.board = board
    self.board.board.set_pin_mode_i2c()

  def scan(self):
    plist = self.board.board.i2c_scan()
    return plist

  def writeto(self, i2c_addr, value):
    self.board.board.i2c_write(i2c_addr, value)

  def readfrom(self, i2c_addr, read_byte):
    return self.board.board.i2c_addr_read(i2c_addr, read_byte)

  def readfrom_mem(self, i2c_addr, reg, read_byte):
    return self.board.board.i2c_read(i2c_addr, reg, read_byte, None)

  def readfrom_mem_restart_transmission(self, i2c_addr, reg, read_byte):
    return self.board.board.i2c_read_restart_transmission(i2c_addr, reg, read_byte, None)

  def writeto_mem(self, i2c_addr, reg, value):
    if isinstance(reg,(list)):
        self.board.board.i2c_write(i2c_addr, reg+list(value))
    else:
        self.board.board.i2c_write(i2c_addr, [reg]+list(value))

class LinuxI2C:
  def __init__(self, board, bus_num=1):
    self.bus_num = bus_num
    print(bus_num)
    self.i2c = I2CMaster(bus_num)

  def scan(self):
    plist=[]
    for i in range(127):
      try:
        ack = self.i2c.transaction(writing(i, []))
        plist.append(i)
      except:
        pass
    return plist

  def writeto(self, i2c_addr, value):
    
    self.i2c.transaction(writing(i2c_addr, value))

  def readfrom(self, i2c_addr, read_byte):
    value = self.i2c.transaction(reading(i2c_addr, read_byte))
    read_buf = []
    for i in range(read_byte):
      read_buf.append(value[0][i])
    return read_buf
 
  def readfrom_mem(self, i2c_addr, reg, read_byte):
    buf = []
    msg = []
    read_buf = []
    buf.append(reg)  
    msg.append(writing(i2c_addr, buf))
    msg.append(reading(i2c_addr, read_byte))  
    value = self.i2c.transaction(*msg)
    for i in range(read_byte):
      read_buf.append(value[0][i])
    return read_buf
  
  def readfrom_mem_restart_transmission(self, i2c_addr, reg, read_byte):
    return self.readfrom_mem(i2c_addr, reg, read_byte)
  
  def writeto_mem(self, i2c_addr, reg, value):
     buf = []
     buf.append(reg)
     buf += value
     self.i2c.transaction(writing(i2c_addr, buf))

class I2C:
  def __init__(self, board=None, bus_num=0):
    if isinstance(board, int):
      bus_num = board
      board = gboard
    elif board == None:
      board = gboard
    self.board = board
    if self.board.i2c[bus_num] == None:
      self.bus_num = bus_num

    if bus_num not in board.res["i2c"]["busnum"]:
      raise ValueError("i2c不支持该设备%d"%bus_num, "支持",board.res["i2c"]["busnum"])
    self.board.i2c[bus_num] = eval(self.board.res["i2c"]["class"] + "(board, bus_num)")
    self.obj = self.board.i2c[bus_num]

  def scan(self):
    return self.obj.scan()

  def writeto(self, i2c_addr, value):
    self.obj.writeto(i2c_addr, value)

  def readfrom(self, i2c_addr, read_byte):
    return self.obj.readfrom(i2c_addr, read_byte)

  def readfrom_mem(self, i2c_addr, reg, read_byte):
    return self.obj.readfrom_mem(i2c_addr, reg, read_byte)

  def readfrom_mem_restart_transmission(self, i2c_addr, reg, read_byte):
    return self.obj.readfrom_mem_restart_transmission(i2c_addr, reg, read_byte)

  def writeto_mem(self, i2c_addr, reg, value):
    return self.obj.writeto_mem(i2c_addr, reg, value)

class TTYUART:
  def __init__(self, board, tty_name, baud_rate):
    self.board = board
    self.uart = serial.Serial(tty_name, baud_rate, timeout=0.1)

  def init(self, baud_rate = 9600, bits = 0, parity = 0, stop = 1):
    pass

  def deinit(self):
    pass

  def writechar(self,data):
    if isinstance(data, str):
      data = ord(data[0])
    self.uart.write(data)

  def write(self, data):
    if isinstance(data, str):
      data = data.encode('utf-8')
    self.uart.write(data)

  def readchar(self):
    return ord(self.uart.read(1))

  def readall(self):
    return self.uart.read(self.uart.inWaiting())

  def readline(self):
    return self.uart.read_until()

  def read(self, n):
    return self.uart.read(n)

  def readinto(self, buf, num = -1):
    buf = self.uart.read(len(buf))

  def any(self):
    return self.uart.inWaiting()

class DuinoUART:
  def __init__(self, board, bus_num, baud_rate):
    self.bus_num = bus_num
    self.board = board
    self.board.board.set_pin_mode_uart(bus_num, baud_rate)

  def init(self, baud_rate = 9600, bits = 0, parity = 0, stop = 1):
    self.board.board.set_pin_mode_uart(self.bus_num, baud_rate, bits, parity, stop)

  def deinit(self):
    self.board.board.uart_deinit(self.bus_num)

  def writechar(self,data):
    return self.board.board.uart_write(self.bus_num,[data])

  def write(self, data):
    self.board.board.uart_write(self.bus_num, data)

  def readchar(self):
    return self.board.board.uart_readchar(self.bus_num)

  def readall(self):
    return self.board.board.uart_readall(self.bus_num)

  def readline(self):
    return self.board.board.uart_readline(self.bus_num)

  def read(self, n):
    return self.board.board.uart_read(self.bus_num, n)

  def readinto(self, buf, num = -1):
    self.board.board.uart_readinto(self.bus_num, buf, num)

  def any(self):
    return self.board.board.uart_any(self.bus_num)

class UART:
  def __init__(self, board=None, tty_name="", bus_num=1, baud_rate=9600):
    if isinstance(board, str):
      baud_rate = bus_num
      bus_num = tty_name
      tty_name = board
      board = gboard
    elif isinstance(board, int):
      bus_num = board
      board = gboard
      self.board = board
    elif board == None:
      board = gboard
      self.board = board
    if self.board.uart[bus_num] == None:
      self.bus_num = bus_num
    if bus_num not in board.res["uart"]["busnum"]:
      raise ValueError("uart不支持该设备%d"%bus_num, "支持",board.res["uart"]["busnum"])
    if self.board.res["uart"]["class"] == "TTYUART":
      self.board.uart[bus_num] = TTYUART(board, tty_name, baud_rate)
    else:
      self.board.uart[bus_num] = DuinoUART(board, bus_num, baud_rate)
    print(self.board.uart)
    self.obj = self.board.uart[bus_num]

  def deinit(self):
    self.obj.deinit()

  def init(self, baud_rate = 9600, bits = 0, parity = 0, stop = 1):
    self.obj.init(baud_rate, bits, parity, stop)

  def writechar(self,data):
    return self.obj.writechar(data)

  def write(self, data):
    print("fasongshujv", data)
    self.obj.write(data)

  def readchar(self):
    return self.obj.readchar()

  def readall(self):
    return self.obj.readall()

  def readline(self):
    return self.obj.readline()

  def read(self, n):
    return self.obj.read(n)

  def readinto(self, buf, num = -1):
    self.obj.readinto(buf, num)

  def any(self):
    return self.obj.any()

class ModBus:
  def __init__(self, board=None, port=None, baudrate=None, host=None, timeout=5):
    self.board = gboard
    if port:
      if port.upper() in list(self.board.modbus.keys()) and self.board.modbus[port]:
        self.master = modbus[port.upper()]
      else:
        ser = serial.Serial(port=port,baudrate=9600, bytesize=8, parity='N', stopbits=1)
        self.master = modbus_rtu.RtuMaster(ser)
        self.ser = ser
        self.board.modbus[port.upper()] = self.master
    elif host:
      host = host.upper()
      if host in list(self.board.modbus.keys()) and self.board.modbus[host]:
        self.master = modbus[host]
      else:
        self.master = modbus_tcp(host=host)
        self.host = host
        self.board.modbus[host] = self.master

    self.master.set_timeout(timeout)
    self.master.set_verbose(True)

  def config_serial(self, baudrate=9600, bytesize=8, parity='N', stopbits=1):
    self.ser.baudrate = baudrate

  def read_holding_reg(self, slave, starting_address, quantity_of_x):
    return self.master.execute(slave, cst.READ_HOLDING_REGISTERS, starting_address, quantity_of_x)

  def read_input_reg(self, slave, starting_address, quantity_of_x):
    return self.master.execute(slave, cst.READ_INPUT_REGISTERS, starting_address, quantity_of_x)

  def read_coils(self, slave, starting_address, quantity_of_x):
    return self.master.execute(slave, cst.READ_COILS, starting_address, quantity_of_x)

  # 读离散输入寄存器
  #logger.info(master.execute(1, cst.READ_DISCRETE_INPUTS, 0, 16))
  def write_single_reg(self, slave, starting_address, output_value):
    return self.master.execute(slave, cst.WRITE_SINGLE_REGISTER, starting_address, output_value=output_value)
        
  def write_multiple_reg(self, slave, starting_address, output_value):
    return self.master.execute(slave, cst.WRITE_MULTIPLE_REGISTERS, starting_address, output_value=output_value)

  def write_multiple_coils(self, slave, starting_address, output_value):
    return self.master.execute(slave, cst.WRITE_MULTIPLE_COILS, starting_address, output_value=output_value)

  #位操作
  def write_single_coil(self, slave, starting_address, output_value):
    return self.master.execute(slave, cst.WRITE_SINGLE_COIL, starting_address, output_value=output_value)

class EVENTIRRecv:
  def __init__(self, board, pin_obj, callback):
    global gthreads
    self.pin_obj = pin_obj
    if not callback:
      raise ValueError("no callback function")
    if not pin_obj:
      raise ValueError("invalid Pin")
    
    inputs = {"NEZHA":{20:"/dev/input/event1"}}
    node= inputs[board.boardname][self.pin_obj.pin]
    #启动一个线程，执行select，发生事件后调用callback函数
    t = threading.Thread(target=self.work,args=(node, callback))
    t.start()
    gthreads.insert(0,t)

  def work(self, node, callback):
    from evdev import InputDevice
    from select import select
    dev = InputDevice(node)
    while True:
      r,w,x = select([dev],[],[],0.2)
      if len(r) == 0:
        continue
      if r[0] == dev:
        for event in dev.read():
          if event.type != 0:
            callback(event.value)

  def read(self):
    return None

class DuinoIRRecv:
  def __init__(self, board, pin_obj, callback):
    self.board = board
    self.pin_obj = pin_obj
    self.board.board.set_pin_mode_ir_recv(self.pin_obj.pin, callback)

  def read(self):
    return self.board.board.ir_read(self.pin_obj.pin)

class IRRecv:
  def __init__(self, board=None, pin_obj=None, callback=None):
    if isinstance(board, Pin):
      callback = pin_obj
      pin_obj = board
    elif callable(board):
      pin_obj = Pin(20)
      callback = board
    if pin_obj.pin in board.res["irrecv"]["pininvalid"]:
      raise ValueError("irrecv不支持该引脚%d"%pin_obj.pin, "不支持引脚名单",board.res["irrecv"]["pininvalid"])
    self.board = gboard   
    self.obj = eval(self.board.res["irrecv"]["class"]+"(self.board, pin_obj, callback)") 
   
  def read(self):
    return self.obj.read()


class RPiIRRemote:
  def __init__(self, board, pin_obj):
    self.pin_obj = pin_obj

  def send(self, value):
    return None

class DuinoIRRemote:
  def __init__(self, board, pin_obj,callback=None):
    self.board = board
    self.pin_obj = pin_obj

  def send(self, value):
    value &= 0xFFFFFFFF      #最多只支持32位
    return self.board.board.ir_send(self.pin_obj.pin, value)

class IRRemote:
  def __init__(self, board=None, pin_obj=None):
    if isinstance(board, Pin):
      pin_obj = board
      board = gboard
    elif board == None:
      board = gboard
    if pin_obj.pin in board.res["irremote"]["pininvalid"]:
      raise ValueError("irremote不支持该引脚%d"%pin_obj.pin, "不支持引脚名单",board.res["irremote"]["pininvalid"])
    self.board = board
    self.obj = eval(self.board.res["irremote"]["class"]+"(self.board, pin_obj)")

  def send(self, value):
    return self.obj.send(value)

class RpiTone:
  def __init__(self, board, pin_obj):
    self.board = board
    self.pwm = PWM(pin_obj = pin_obj)
    self.freq_value = 0

  def on(self):
    self.pwm.freq(self.freq_value)

  def off(self):
    self.pwm.freq(0)

  def freq(self, v=None):
    if v == None:
      return self.freq_value
    else:
      self.freq_value = v
      self.pwm.freq(v)

  def tone(self, freq, duration):
#    self.pwm.play_tone(self.pin_obj.pin, freq, duration) 
     pass
                                                     #*****封装模块库
class DuinoTone:
  def __init__(self, board, pin_obj):
    self.board = board
    self.pin_obj = pin_obj
    self.board.board.set_pin_mode_tone(self.pin_obj.pin)
    self.freq_value = 100
    
  def on(self):
   
    if self.board.res["tone"]["type"] == "dfrobot_firmata": 
      self.board.board.dfrobot_play_tone(self.pin_obj.pin, self.freq_value, 0)
    self.board.board.play_tone(self.pin_obj.pin, self.freq_value, 0)

  def off(self):
    
    if self.board.res["tone"]["type"] == "dfrobot_firmata":
      self.board.board.dfrobot_play_tone(self.pin_obj.pin, 0, 0)
    self.board.board.play_tone(self.pin_obj.pin, 0, 0)

  def freq(self, v=None):
    if v == None:
      return self.freq_value
    else:
      if isinstance(v, float):
        raise TypeError("decimals are not supported")
      elif v < 0:
        raise TypeError("negative numbers are not supported")
      else:
        self.freq_value = v

  def tone(self, freq, duration):
    
    if self.board.res["tone"]["type"] == "dfrobot_firmata":
      self.board.board.dfrobot_play_tone(self.pin_obj.pin, freq, duration)
      self.board.board.play_tone(self.pin_obj.pin, freq, duration)
    else:
      if duration > 0:
        self.freq_value = freq
        self.on()
        start = time.time()
        while time.time() - start < duration / 1000:
          pass
        self.off()
      else:
        self.board.board.play_tone(self.pin_obj.pin, freq, duration)

class Tone:
  def __init__(self, board=None, pin_obj=None):
    if isinstance(board, Pin):
      pin_obj = board
      board = gboard
    elif board == None:
      board = gboard
    self.board = board  
    if pin_obj.pin in board.res["tone"]["pininvalid"]:
      raise ValueError("tone不支持该引脚%d"%pin_obj.pin, "不支持引脚名单",board.res["tone"]["pininvalid"])
    self.obj = eval(board.res["tone"]["class"]+"(board, pin_obj)")

  def on(self):
    self.obj.on()

  def off(self):
    self.obj.off()

  def freq(self, v=None):
    if v == None:
      return self.obj.freq(v)
    else:
     self.obj.freq(v)

  def tone(self, freq, duration):
    self.obj.tone(freq=freq,duration=duration)

class RPiServo:
  def __init__(self, board, pin_obj):
    self.board = board
    self.pin_obj = pin_obj
    GPIO.setup(self.pin_obj.pin, GPIO.OUT)
    self.pwm=GPIO.PWM(self.pin_obj.pin, 50)
    self.pwm.start(0)

  def write_angle(self, value):
    self.angle(value)
    
  def angle(self, _angle):
    duty = int(_angle*(10.0/180.0)+2.5)
    self.pwm.ChangeDutyCycle(duty)
  
  def detach(self):
    self.pwm.stop()
    self.pwm = None
    GPIO.setup(self.pin_obj.pin, GPIO.IN)

class SYSFSServo:
  def __init__(self, board, pin_obj):
    self.board = board
    self.pin_obj = pin_obj
    self.pwm=SYSFSPWM(board, pin_obj)
    self.pwm.freq(50)

  def write_angle(self, value):
    self.angle(value)
    
  def angle(self, _angle):
    #duty_value = int(_angle*(10.0/180.0)+2.5)
    duty_value = _angle*(10.0/180.0)+2.5
    self.pwm.duty(duty_value)
  
  def detach(self):
    self.pwm.deinit()

class DuinoServo:
  def __init__(self, board, pin_obj):
    self.board = board
    self.pin_obj = pin_obj
    self.board.board.set_pin_mode_servo(self.pin_obj.pin)
    self.board.board.set_mode_servo(self.pin_obj.pin)

  def write_angle(self, value):
    self.angle(value)
  
  def angle(self, _angle):
  
    if self.board.res["servo"]["type"] == "dfrobot_firmata":
      if self.pin_obj.pin < 16:
        self.board.board.servo_write(self.pin_obj.pin, _angle)
      else:
        self.board.board.dfrobot_servo_write(self.pin_obj.pin, _angle)
    else:
      self.board.board.servo_write(self.pin_obj.pin, _angle)
  
  def detach(self):
    self.board.set_pin_mode_digital_input(self.pin_obj.pin, callback=None)

class Servo:
  def __init__(self, board=None, pin_obj=None):
    if isinstance(board, Pin):
      pin_obj = board
      board = gboard
    elif board == None:
      board = gboard
    
    self.board = board
    self.pin_obj = pin_obj
    if pin_obj.pin in board.res["servo"]["pininvalid"]:
      raise ValueError("servo不支持该引脚%d"%pin_obj.pin, "不支持引脚名单",board.res["servo"]["pininvalid"])
    self.obj = eval(board.res["servo"]["class"]+"(board, pin_obj)")

  def write_angle(self, value):
    self.obj.write_angle(value)
  
  def angle(self, _angle):
    self.obj.angle(_angle)
  
  def detach(self):
    self.obj.detach()

class NeoPixel(NeoPixelExtension):
  def __init__(self, board=None, pin_obj=None, num=None):
    if isinstance(board, Pin):
      num = pin_obj
      pin_obj = board
      board = gboard
    elif board == None:
      board = gboard

    NeoPixelExtension.__init__(self, board, pin_obj, num)

class DHT11(DHT11Extension):
  def __init__(self,board=None, pin_obj=None):
    
    if isinstance(board, Pin):
      pin_obj = board
      board = gboard
      
    elif board == None:
      board = gboard
    DHT11Extension.__init__(self, board, pin_obj)

class DHT22(DHT11Extension):
  def __init__(self,board=None, pin_obj=None): 
    if isinstance(board, Pin):
      pin_obj = board
      board = gboard

    elif board == None:
      board = gboard
    DHT22Extension.__init__(self, board, pin_obj)

class SR04_URM10(SR04_URM10Extension):
  def __init__(self,board=None, trigger_pin_obj=None, echo_pin_obj=None):
    if isinstance(board, Pin):
      echo_pin_obj = trigger_pin_obj
      trigger_pin_obj = board
      board = gboard
    elif board == None:
      board = gboard
    SR04_URM10Extension.__init__(self, board, trigger_pin_obj, echo_pin_obj)

class DS18B20(DS18B20Extension):
  def __init__(self, board=None, pin_obj=None):
    if isinstance(board, Pin):
      pin_obj = board
      board = gboard
    elif board == None:
      board = gboard
    DS18B20Extension.__init__(self, board, pin_obj)

class GP2Y1010AU0F(GP2Y1010AU0FExtension): #空气质量粉尘传感器 仅unihiker
  def __init__(self, board=None, anapin=None, digpin=None):
    if isinstance(board, int):
      digpin = anapin
      anapin = board
      board = gboard
    elif board == None:
      board = gboard
    GP2Y1010AU0FExtension.__init__(self, board, anapin, digpin)

class AudioAnalyzer(AudioAnalyzerExtension):
   def __init__(self, board=None, strobe=None, RST=None, DC=None):
    if isinstance(board, int):
      strobe_pin = board
      RST_pin = strobe
      DC_pin = RST
      board = gboard
    elif board == None:
      board = gboard
    AudioAnalyzerExtension.__init__(self, board, strobe_pin, RST_pin, DC_pin)
#firmata 协议支持的模块
class HX711(HX711Extension):
   def __init__(self, board, dout_pin, sck_pin = 2121, scale = None):
    if isinstance(board, int):
      scale = sck_pin
      sck_pin = dout_pin
      dout_pin = board
      board = gboard
    elif board == None:
      board = gboard
    HX711Extension.__init__(self,  board, dout_pin, sck_pin, scale)

class Board:
  def __init__(self, boardname="", port=None):
    
    global gboard
    gboard = None
    self.boardname = boardname.upper()
    self.port = port
    self.connected = False
    self.timeout = 0
    self.res = {}
   
    self.i2c = [None, None, None, None, None]
    self.uart = [None, None, None, None, None]
    self.modbus = {}
    self.spi = [[None, None], [None, None]]
    print("pinpong V0.2")
    
    signal.signal(signal.SIGINT, self._exit_handler)

    if self.res == None:
      pass ###########
      return

    if platform.platform().find("rockchip") > 0:  ###############如果上面插了一个uno怎么办？

      self.boardname = "UNIHIKER"####验收的时候讨论下这句话是否可以去掉
    
    
    print(self.boardname)
    self.res = get_globalvar_value(self.boardname)
    
    if gboard == None:
      gboard = self
      self.res[self.boardname] = gboard
    
    self.res["init"](self, boardname, port)

  def begin(self):
    version = sys.version.split(' ')[0]
    plat = platform.platform()
    if self.connected: #Linux or Win SBC
      return self

    self.res["begin"](self)
    major,minor = self.detect_firmata()
    
    print("[32] Firmata ID: %d.%d"%(major,minor))
    if (major,minor) != firmware_version[self.boardname]:#burn new firmware
      FIRMATA_MAJOR = firmware_version[self.boardname][0]
      FIRMATA_MINOR = firmware_version[self.boardname][1]
      self.serial.close()
      self.serial = self.port
      print("[35] Burning firmware...")
      cwdpath,_ = os.path.split(os.path.realpath(__file__))
      self.pgm = Burner(self.boardname,self.port)
      self.res["find_port"](self)
      print(self.res["firmware"])
      
      self.pgm.burn(cwdpath + self.res["firmware"][0]+str(FIRMATA_MAJOR)+"."+str(FIRMATA_MINOR)+self.res["firmware"][1])

    
      time.sleep(2)
      print("[37] Burn done")
      self.detect_firmata()  
    self.board = pymata4.Pymata4(com_port=self.serial, arduino_wait=2, baud_rate=115200, name = self.boardname)
    self.connected = True
    return self
  
  def detect_firmata(self):
  
    vidpid={
    "UNO":"2341:0043",
    "LEONARDO":"3343:8036",
    "LEONARDO":"2341:8036",
    "MEGA2560":"2341:0042",
    "MICROBIT":"0D28:0204",
    "HANDPY":"10C4:EA60",
    "HANDPY":"1A86:55D4"       #兼容新版掌控
    }
    findboard={
    "VID:PID=2341:0043":"UNO",
    "VID:PID=3343:8036":"LEONARDO",
    "VID:PID=2341:8036":"LEONARDO",
    "VID:PID=2341:0042":"MEGA2560",
    "VID:PID=0D28:0204":"MICROBIT",
    "VID:PID=10C4:EA60":"HANDPY",
    "VID:PID=1A86:55D4":"HANDPY"
    }
    _vidpid = ''''''
    self.duration={
    "UNO": 0.1,
    "LEONARDO": 0.1,
    "LEONARDO": 0.1,
    "MEGA2560":0.5,
    "MICROBIT": 0.5,
    "HANDPY": 0.5,
    "HANDPY": 0.5,
    "UNIHIKER": 0.1
    }
    portlist=[]
    localportlist=[]
    
    if self.port == None and self.boardname != "":
      plist = list(serial.tools.list_ports.comports())
      for port in plist:
        msg = list(port)
        if msg[2].find(vidpid[self.boardname]) >= 0:
          portlist.insert(0,msg)
          break
        elif msg[2].find("USB") >= 0:
          portlist.insert(0,msg)
        else:
          localportlist.append(msg)
        portlist += localportlist
      if len(portlist) > 0:
        self.port = portlist[0][0]
    elif self.boardname == "" and self.port != None:
      plist = list(serial.tools.list_ports.comports())
      for port in plist:
        msg = list(port)
        if msg[0] == self.port:
          vidpid = msg[2].split(" ")
          if len(vidpid) > 2 and vidpid[1] in _vidpid:
            self.boardname = findboard[vidpid[1]]
            self.port = msg[0]
            break
    else:
      plist = list(serial.tools.list_ports.comports())
      for port in plist:
        msg = list(port)
        vidpid = msg[2].split(" ")
        if len(vidpid) > 2 and vidpid[1] in _vidpid:
          self.boardname = findboard[vidpid[1]]
          self.port = msg[0]
    print("selected -> board: %s serial: %s"%(self.boardname, self.port))
    if self.port == None:
      return 0,0
    print("[10] Opening "+self.port)
    name = platform.platform()
    
    self.res["reset"]()
    
    self.res["open_serial"](self)
  
    self.serial.read(self.serial.in_waiting)
    buf=bytearray(b"\xf0\x79\xf7")
    self.serial.write(buf)
    res = self.serial.read(5)
    major=0
    minor=0
    
    if len(res) >=3 and res[0] == 0xF0 and res[1] == 0x79:
      major = res[2]
      minor = res[3]
   
    if (major,minor) == (FIRMATA_MAJOR,FIRMATA_MINOR):
   
      self.res["soft_reset"](self)
     
    return major,minor
  
  def disconnect(self):
    self.board.disconnect()

  def _exit_handler(self, signum, frame):
    global gthreads
    print("exit_handler")
    for thread in gthreads:
        _async_raise(thread.ident, SystemExit)
    sys.exit(0)

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    try:
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            # pass
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")
    except Exception as err:
        print(err)
