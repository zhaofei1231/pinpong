# -*- coding: utf-8 -*- 

import platform
import serial
import sys
import subprocess
import re

from pinpong.extension.globalvar import *
from pinpong.base.comm import *

mic_res = {
    "i2c" : None,

    "pin" : {
        "type" : "dfrobot",
        "class" : "DuinoPin",
        "pinnum" : True        
        },
    "tone" : {
        "type" : "dfrobot",
        "class" : "DuinoTone"
        },
    "servo" : {
        "type" : "dfrobot",
        "class" : "DuinoServo"
        },
    "dht" : {
        "type" : "dfrobot"       
        },
    "adc" : {
        "type" : "dfrobot",
        "class" : "DuinoADC"  
        },
    "pwm" : {
        "type" : "dfrobot",
        "class" : "DuinoPWM"
        },
    "dht11" : "dfrobot",
    "dht22" : "dfrobot"
           
    }
def init(board, boardname, port):
    printlogo()
    board.connected = False

    
def differ_microbit():       #区分microbit V1 V2
    if sys.platform == 'win32':
      try:
        disks = subprocess.Popen(
        "wmic logicaldisk get deviceid, description", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.read().decode('utf-8').split("\n")
      except Exception:
        disks = subprocess.Popen(
        "wmic logicaldisk get deviceid, description", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.read().decode('gbk').split("\n")
      for disk in disks:
        if 'Removable' in disk or '可移动磁盘' in disk:
          d=re.search(r'\w:', disk).group()
          diskname = subprocess.Popen(
      "wmic logicaldisk where name='%s' get volumename"%(d), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.read().decode('utf-8').split("\n")
          if "MICROBIT" in diskname[1]:
            mount_point = d+"/"
            file = mount_point + "DETAILS.TXT"
            file = open(file, mode='r')
            info = file.readlines()
            val = int(info[1][11:15])
            if val >= 9904:
              return "MICROBITV2"
      return "MICROBITV1"
    elif sys.platform == 'linux':
      message=""
      with open('/proc/mounts', 'r') as f:
        while True:
          l = f.readline()
          if l == "":
            break
          elif "MICROBIT" in l:
            message=l
        if message != "":
          mount_point = message.split(" ")[1]+"/" + "DETAILS.TXT"
          with open(mount_point, 'r') as file:
            info = file.readlines()
            val = int(info[1][11:15])
            if val >= 9904:
              return "MICROBITV2"
        return "MICROBITV1"
    elif sys.platform == 'darwin':
      result = subprocess.Popen(
      "ls /Volumes", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.read().decode('utf-8').split()
      if 'MICROBIT' in result:
        mount_point = "/Volumes/MICROBIT/"+ "DETAILS.TXT"
        with open(mount_point, 'r') as file:
          info = file.readlines()
          val = int(info[1][11:15])
          if val >= 9904:
            return "MICROBITV2"
      else:
        mount_point = None
        return "MICROBITV1"
        
def begin(board):
    
    name = differ_microbit()
    print("mic = ", name)
    if name == "MICROBITV1":
      mic_res["firmware"] = ["/base/FirmataExpress.MICROBIT.", ".hex"]
    else:
      mic_res["firmware"] = ["/base/FirmataExpress.MICROBITV2.", ".hex"]        
        
        
        
def open_serial(board):
  board.serial = serial.Serial(board.port, 115200, timeout=board.duration[board.boardname])
  
  
def soft_reset(board):
  board.serial.read(board.serial.in_waiting)
  reset_buf=bytearray(b"\xf0\x0d\x55\xf7")
  board.serial.write(reset_buf)
  reset = board.serial.read(1024)
  
mic_res["init"] = init
mic_res["begin"] = begin
mic_res["open_serial"] = open_serial
mic_res["soft_reset"] = soft_reset  
  
  
  
set_globalvar_value("MICROBIT", mic_res)