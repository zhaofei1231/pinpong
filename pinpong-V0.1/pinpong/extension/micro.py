# -*- coding: utf-8 -*- 

mic_res = {
    
    "tone" : {
        type : "dfrobot",
        "class" : "DuinoTone"
        },
    "servo" : {
        type : "dfrobot",
        "class" : "DuinoServo"
        },
    "dht" : {
        type : "dfrobot",
        
        }
    "adc" : {
        type : "dfrobot",
        "class" : "DunioADC",
        
        }
         
    }
def init(board, boardname, port):
    printlogo()
    board.connected = False

def begin(board):
    
    name = deffer_microbit()
    if name == "MICROBITV1":
      mic_res["firmware"] = ["/base/FirmataExpress.MICROBIT.", ".hex"]
    else:
      mic_res["firmware"] = ["/base/FirmataExpress.MICROBITV2.", ".hex"]
    
def differ_microbit(self):       #区分microbit V1 V2
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
              return True
      return False
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
              return True
        return False
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
        
def open_serial(board):
  self.serial = serial.Serial(self.port, 115200, timeout=board.duration[self.boardname])
  
  
def soft_reset(board):
  board.serial.read(board.serial.in_waiting)
  reset_buf=bytearray(b"\xf0\x0d\x55\xf7")
  board.serial.write(reset_buf)
  reset = board.serial.read(1024)