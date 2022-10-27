# -*- coding: utf-8 -*- 
from comm import method

def RpiPininit(pin=None):
  method.clear()
  
  if pin == None:
    return 
  export_path = '/sys/class/gpio/export'
  value_path = '/sys/class/gpio/gpio'+str(pin)+'/value'
  direction_path = '/sys/class/gpio/gpio'+str(pin)+'/direction'

  if not os.path.exists('/sys/class/gpio/gpio'+str(pin)):
    os.system('echo '+str(pin)+' > '+export_path)
 
  method["Pin.OUT"] = "os.system('echo out > ' + self.direction_path)"
  method["Pin.IN"] = "os.system('echo in > ' + self.direction_path)"
  method["Pin.PWM"] = ["GPIO.setup(self.pin, GPIO.OUT)", "self.pwm=GPIO.PWM(self.pin, 1000)"]
  method["Pin.ANALOG"] = "self.board.board.set_pin_mode_analog_input(self.apin, None)"
    
  
