# -*- coding: utf-8 -*- 

uni_res = {
  "init" : init,
  "begin" : begin,
  "reset" : reset,
  "servo" : {
      type : "dfrobot"
      "class" : "DuinoServo"
      }
  }

def init(board, boardname, port):
  printlogo()
  board.connected = False
  
def begin():
  uni_res["firmware"] = ["/base/FirmataExpress.UNIHIKER.", ".bin"]
  


def reset():
  if not os.path.exists("/sys/class/gpio/gpio80"):
    os.system("echo 80 > /sys/class/gpio/export")#RST
  if not os.path.exists("/sys/class/gpio/gpio69"):
   os.system("echo 69 > /sys/class/gpio/export")#BOOT0      
  os.system("echo out > /sys/class/gpio/gpio69/direction")
  os.system("echo out > /sys/class/gpio/gpio80/direction")
  os.system("echo 0 > /sys/class/gpio/gpio69/value")
  os.system("echo 1 > /sys/class/gpio/gpio80/value")
  os.system("echo 0 > /sys/class/gpio/gpio80/value")
  os.system("echo 1 > /sys/class/gpio/gpio80/value")
  
set_globalvar_value("UNIHIKER", uni_res)