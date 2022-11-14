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
 
 