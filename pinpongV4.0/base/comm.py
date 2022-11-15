# -*- coding: utf-8 -*-
PINPONG_MAJOR=0
PINPONG_MINOR=4
PINPONG_DELTA=9

FIRMATA_MAJOR = 2
FIRMATA_MINOR = 7


firmware_version = {
  "UNO":(2,7),
  "LEONARDO":(2,7),
  "MEGA2560":(2,7),
  "MICROBIT":(2,7),
  "HANDPY":(2,7),
  "UNIHIKER":(3,3)
}

def printlogo_big():
    print("""
  __________________________________________
 |    ____  _       ____                    |
 |   / __ \(_)___  / __ \____  ____  ____ _ |
 |  / /_/ / / __ \/ /_/ / __ \/ __ \/ __ `/ |
 | / ____/ / / / / ____/ /_/ / / / / /_/ /  |
 |/_/   /_/_/ /_/_/    \____/_/ /_/\__, /   |
 |   v%d.%d.%d  Designed by DFRobot  /____/    |
 |__________________________________________|
 """%(PINPONG_MAJOR,PINPONG_MINOR,PINPONG_DELTA))


def printlogo():
    print("""
  ___________________________
 |                           |
 |      PinPong v%d.%d.%d       |
 |    Designed by DFRobot    |
 |___________________________|
 """%(PINPONG_MAJOR,PINPONG_MINOR,PINPONG_DELTA))
 
class PinInformation:
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