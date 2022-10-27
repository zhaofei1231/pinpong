# -*- coding: utf-8 -*-
#linux 板通信接口信息


duino_comm_res = {
    "pinin":,[D0,D1,D2,D3,D4,D5,D6,D7,D8,D9,D10,D11,D12,D13],
    "pinout":[D0,D1,D2,D3,D4,D5,D6,D7,D8,D9,D10,D11,D12,D13],
    "pinanalog":[A0,A1,A2,A3,A4,A5],
    "spi" : [0],
}



Com = {
  
    "_i2c_init" : [False,False,False,False,False], 
    "i2c" : [None, None, None, None, None], 
    "uart" : [None, None, None, None, None], 
    "modbus" : {},
    "_spi_init" : [[False,False], [False,False]],
    "spi" : [[None, None], [None, None]],
    "i2c_fixed" : {"RPI":1,"NEZHA":2,"JH7100":1} 
  }
  
#板子初始化判断信息
 
DuinoBoard = []

{  
  "boardname" : "",
  "connect" : False,
  "port" : None,
  "spi_wifi_uno" : False
  }

#板子烧录信息

firm = {
      "UNO_PB" : ["/base/FirmataExpress.UNO_PB.", ".hex"],
      "UNO" : ["/base/FirmataExpress.UNO.", ".hex"],
      "LEONARDO" : ["/base/FirmataExpress.LEONARDO.", ".hex"],
      "MEGA2560" : ["/base/FirmataExpress.MEGA2560.", ".hex"],
      "HANDPY" : ["/base/FirmataExpress.HANDPY.", ".bin"],
      "MICROBITV1" : ["/base/FirmataExpress.MICROBIT.", ".hex"],
      "MICROBITV2" : ["/base/FirmataExpress.MICROBITV2.", ".hex"],
      "UNIHIKER" : ["/base/FirmataExpress.UNIHIKER.", ".bin"]
    }
    
#通用linux板

  
inux_board_list = ["RPI", "WIN", "JH7100", "XUGU", "PINPONG"]

#引脚信息
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
nezha_pinmap = [None,33,32,118,40,41,2027,37,   2020,44,2021,2022,108,109,2024,107,    106,2023,110,2025,111,65,38,2026,    35,36]
jh7100_pinmap = [448,449,450,451,452,None,454,10000,#0
                   456,457,458,None,None,None,None,None,#8
                   None,465,None,467,468,469,470,None,#16
                   None,None,None,None,None,None,None,None,#24
                   None,None,None,None,None,None,None,None,#32
                   None,None,None,None,None,None,494,None,#40
                   None]#48


#引脚初始化方法
method = {}