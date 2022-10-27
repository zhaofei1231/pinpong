# -*- coding: utf-8 -*-
from globalvar import *
from comm import *

#uno_res["pwm"]=[2,4]
uno_res = {
    "pwm" : [2,4],
    "i2c" : [0], 
    "uart" : [0],
    "begin" : begin,
    "init" : init
    "pin" : {
        type : "general",
        "class" : "DuinoPin",
        "pinnum" : False,
        "pinmap" : [D0, D1, D3, D4, D5, D6, D7, D8, D9, D10, D11, D12, D13, 
        A0, A1, A2, A3, A4, A5]
        },
    "pwm" : {
        "pwminit" : pwminit,
        "pwmfreq" : pwmfreq,
        "pwmduty" : pwmduty,
        "pwmdeinit" : pwminit
        }
    }
uno_res = duino_comm_res.update(uno_res)
#

def begin(board):
  version = sys.version.split(' ')[0]
  plat = platform.platform()
  if board.boardname == "PinPong Board":
    print("[01] Python"+version+" "+plat+" Board: "+ "PinPong Board")
    uno_res.update["firmware"] = ["/base/FirmataExpress.UNO_PB.", ".hex"]
  else:
    print("[01] Python"+version+" "+plat+(" " if self.boardname == "" else " Board: "+ self.boardname))
    if name.find("Linux_vvBoard_OS")>=0 or name.find("Linux-4.4.159-aarch64-with-Ubuntu-16.04-xenial")>=0:
      cmd = "/home/scope/software/avrdude-6.3/avrdude -C/home/scope/software/avrdude-6.3/avrdude.conf -v -patmega328p -carduino -P"+self.port+" -b115200 -D -Uflash:w:"+cwdpath + "/base/FirmataExpress.UNO."+str(FIRMATA_MAJOR)+"."+str(FIRMATA_MINOR)+".hex"+":i"
      os.system(cmd)
    else:
      uno_res.update["firmware"] = ["/base/FirmataExpress.UNO.", ".hex"]
  
#资源初始化
#打印logo
#  
def init(board, boardname, port):
  if port == 8081:#wifi port
      printlogo_big()
      self.ip = boardname
      self.port = port
      self.boardname = "UNO"
      self.board = pymata4.Pymata4(ip_address=self.ip, ip_port=self.port)
      self.board.i2c_write(0x10, [0,0,0])
      self.board.i2c_write(0x10, [2,0,0])

    name = platform.platform()
    board.connected = False #验证一下是值传递还是引用传递

def reset():
  pass

def reset_delay():
  time.sleep(2)

def pwminit(board, pin_obj):
  board.board.board.set_pin_mode_pwm_output(board.pin_obj.pin)

def pwmfreq(board):
  real_duty = int(self.duty_value / 255 * 100)
  real_duty = 255 if real_duty>255 else real_duty
  board.board.board.pwm_write(board.pin_obj.pin, board.freq_value, real_duty)

def pwmduty(board):
  real_duty = int(self.duty_value / 255 * 100)
  real_duty = 255 if real_duty>255 else real_duty
  self.board.board.pwm_write(self.pin_obj.pin, self.freq_value, real_duty)


def pwmdeinit(board):
  board.board.pin_obj.pin_mode(Pin.IN)
  
  
  
set_globalvar_value("uno", uno_res)
