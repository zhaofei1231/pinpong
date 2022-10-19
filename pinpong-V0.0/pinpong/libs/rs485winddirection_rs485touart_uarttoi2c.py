# -*- coding: utf-8 -*-
from pinpong.board import gboard,UART
from pinpong.libs.dfrobot_uarttoi2c import DFRobot_IIC_Serial
import time

class IICSerialWindDirection:
    ## Sub UART channel1 
    SUBUART_CHANNEL_1   = 0x00
    ## Sub UART channel2   
    SUBUART_CHANNEL_2   = 0x01
    ## All sub channels   
    SUBUART_CHANNEL_ALL = 0x11
    DIRECTION = {
            0:"北",
            1:"东北偏北",
            2:"东北",
            3:"东北偏东",
            4:"东",
            5:"东南偏东",
            6:"东南",
            7:"东南偏南",
            8:"南",
            9:"西南偏南",
            10:"西南",
            11:"西南偏西",
            12:"西",
            13:"西北偏西",
            14:"西北",
            15:"西北偏北"
        }
    def __init__(self, sub_uart_channel=0x00, IA1=1, IA0 = 1):
        self.uart = DFRobot_IIC_Serial(sub_uart_channel, IA1, IA0)
        self.uart.begin(baud = 9600, format = self.uart.IIC_Serial_8N1)
        self.addr2 = 0

    def read_wind_direction(self):
        Address = self.addr2
        index = self._read_wind_direction(Address)
        try:
            return self.DIRECTION[index]
        except:
            return -1

    def _read_wind_direction(self, Address):
        COM = [0x00, 0x03, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00]
        COM[0] = Address
        Winddirection = -1
        self.addedCRC(COM, 6)
        self.readall()
        self.uart.write(COM)
        timeout = time.time()
        while True:
            if(self.uart.available() == 7):
                break
            else:
                if(time.time() - timeout > 2):
                    return -1
        data = self.readall()
        if(self.CRC16_2(data, 5) == data[5] * 256 + data[6]):
            Winddirection = (data[3] * 256 + data[4])
        return Winddirection

    def modify_address(self, addr1, addr2):
        self.addr2 = addr2
        buf = [0x00, 0x10, 0x10, 0x00, 0x00, 0x01, 0x02, 0x00, 0x00, 0x00, 0x00]
        ret = False
        curr = time.time()
        buf[0] = addr1
        buf[8] = addr2
        self.addedCRC(buf, 9)
        time.sleep(0.1)
        self.readall()
        self.uart.write(buf)
        time.sleep(1)
        timeout = time.time()
        while True:
            # print(self.uart.available())
            if(self.uart.available() == 8):
                break
            elif time.time() - timeout > 3:
                return False
        rxbuf = self.readall()
        if(rxbuf[0] == addr1 and rxbuf[1] == 0x10 and rxbuf[2] == 0x10 and rxbuf[3] == 0x00 and rxbuf[4] == 0x00 and rxbuf[5] == 0x01):
            ret = True
        return ret

    def readall(self):
        c = []
        while self.uart.available():
            c.append(self.uart.read())
        return c

    def addedCRC(self, buf, len):
        crc = 0xFFFF
        for pos in range(len):
            crc ^= buf[pos]
            for i in range(8, 0, -1):
                if((crc & 0x0001) != 0):
                   crc >>= 1
                   crc ^= 0xA001
                else:
                    crc >>= 1
        buf[len] = crc % 0x100
        buf[len+1] = crc // 0x100

    def CRC16_2(self, buf, len):
        crc = 0xFFFF
        for pos in range(len):
            crc ^= buf[pos]
            for i in range(8, 0, -1):
                if((crc & 0x0001) != 0):
                   crc >>= 1
                   crc ^= 0xA001
                else:
                    crc >>= 1
        crc = ((crc & 0x00ff) << 8) | ((crc & 0xff00) >> 8)
        return crc
