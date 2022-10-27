# -*- coding: utf-8 -*-


# -*- coding: utf-8 -*-
from globalvar import *
from comm import *

leo_res = duino_comm_res
leo_res = {
    "pinin":,[D0,D1,D2,D3,D4,D5,D6,D7,D8,D9,D10,D11,D12,D13],
    "pinout":[D0,D1,D2,D3,D4,D5,D6,D7,D8,D9,D10,D11,D12,D13],
    "pinanalog":[A0,A1,A2,A3,A4,A5],
    "pwm":[2,4],
    "i2c" : [0], 
    "uart" : [0],
    "spi" : [0],
    "pin" : {
        type : "general",
        "class" : "DuinoPin",
        "pinnum" : False,
        "pinmap" : [D0, D1, D3, D4, D5, D6, D7, D8, D9, D10, D11, D12, D13, 
        A0, A1, A2, A3, A4, A5]
        },
    "pwm" : {
        "class" : "DuinoPWM",
        type:"general",
        
        },
   
      
}


def init(board, boardname, port):
    printlogo()
    name = platform.platform()
    board.connected = False #验证一下是值传递还是引用传递


def begin(board):
    
    leo_res["firmware"] = ["/base/FirmataExpress.LEONARDO.", ".hex"]
    port_list_0 = list(serial.tools.list_ports.comports())
    port_list_2 = port_list_0 = [list(x) for x in port_list_0]
    ser = serial.Serial(self.port,1200,timeout=1) #复位
    ser.close()
    time.sleep(0.2)
    retry = 5
    port = None
    while retry:
      retry = retry - 1

      port_list_2 = list(serial.tools.list_ports.comports())
      port_list_2 = [list(x) for x in port_list_2]
      for p in port_list_2:
        if p not in port_list_0:
          port = p
          break
      if port == None:
        time.sleep(0.5)
      if port: #找到了BootLoader串口
        break
    if port == None:
      print("[99] can NOT find ",self.boardname)
      sys.exit(0)
    board.pgm = Burner(self.boardname, port[0])
   

#复位板子
#使用1200波特率打开串口，再用1200波特率关闭串口
def reset(board):
  s = serial.Serial(board.port, 1200)
  s.close()
  time.sleep(8)

def open_serial(board):
  board.serial = serial.Serial(board.port, 115200, timeout=board.duration[board.boardname])
  
def soft_reset(board):
  pass




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

def irinit(board, pin_obj, callback):
  board.board.board.set_pin_mode_ir_recv(pin_obj.pin, callback)
        
def irread(board):
  board.board.board.ir_read(board.pin_obj.pin)

def irsend(board, value):
  value &= 0xFFFFFFFF
  return board.board.board.ir_send(board.pin_obj.pin, value)

set_globalvar_value("leonardo", leo_res)