# -*- coding: utf-8 -*- 
import comm

han_res = {
    "pinin" : ,
    "pinout" : ,
    "pinanalog" :,
    "init" : init,
    "begin" : begin,
    "adc" : {
        type : "dfrobot",
        "class" : "DunioADC",
        
        }
    
    }
  
def init(board, boardname, port):
  printlogo()
  board.connected = False
  
def begin(board)
  han_res["firmware"] = ["/base/FirmataExpress.HANDPY.", ".bin"]

def open_serial(board):
  if sys.platform == "win32":
    self.serial = serial.Serial(self.port, 115200, dsrdtr = True, rtscts =True, timeout=board.duration[board.boardname])
  else:
    self.serial = serial.Serial(self.port, 115200, timeout=board.duration[board.boardname])

def sort_reset(board):
  board.serial.read(board.serial.in_waiting)
  reset_buf=bytearray(b"\xf0\x0d\x55\xf7")
  board.serial.write(reset_buf)
  reset = board.serial.read(1024)


  
set_globalvar_value("handpy", han_res)