# -*- coding: utf-8 -*- 

nez_res = {
    "begin" : begin 
    "init" : init,
    "pin" : {
        type : "general",
        "class" : "SYSFSPin",
        "pinmap" : [None,33,32,118,40,41,2027,37,   2020,44,2021,2022,108,109,2024,107,    106,2023,110,2025,111,65,38,2026,    35,36]
        },
    "pwm" : {
        type : "general",
        "class" : "SYSFSPWM",
        "pinnum" : True,
        "GPIO" : [22, 3],
        "config" : {
            22 : {"channel" : 1, "io" : 38},
            3 : {"channel" : 7, "io" : 118}
            }
        }
    "servo" : {
        type : "general",
        "class" : "SYSFSServo"
        }
    }


def init(board, boardname, port):
  printlogo()
  board.connected = True
  
def begin(board):
  version = sys.version.split(' ')[0]
  plat = platform.platform()
  print("[01] Python"+version+" "+plat+(" " if board.boardname == "" else " Board: "+ board.boardname))  




set_globalvar_value("NEZHA", nez_res)  
