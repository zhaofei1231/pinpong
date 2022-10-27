# -*- coding: utf-8 -*- 
from comm import method

def RpiPininit():
  method.clear()
  method["Pin.OUT"] = "GPIO.setup(self.pin, GPIO.OUT)"
  method["Pin.IN"] = "GPIO.setup(self.pin, GPIO.IN)"
  method["Pin.PWM"] = ["GPIO.setup(self.pin, GPIO.OUT)", "self.pwm=GPIO.PWM(self.pin, 1000)"]
  method["Pin.ANALOG"] = "self.board.board.set_pin_mode_analog_input(self.apin, None)"
    
  
