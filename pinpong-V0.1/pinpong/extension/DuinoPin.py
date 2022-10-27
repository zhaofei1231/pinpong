# -*- coding: utf-8 -*- 
from comm import method

def DuinoPininit():
  method.clear()
  method["Pin.OUT"] = "self.board.board.set_pin_mode_digital_output(self.pin)"
  method["Pin.IN"] = "self.board.board.set_pin_mode_digital_input(self.pin, callback=None)"
  method["Pin.PWM"] = "self.board.board.set_pin_mode_pwm_output(self.pin)"
  method["Pin.ANALOG"] = "self.board.board.set_pin_mode_analog_input(self.apin, None)"
  method["read"] = "self.val = self.board.board.digital_read(self.pin)"
  method["write"] = "self.board.board.digital_pin_write(self.pin, v)"
  
