# -*- coding: utf-8 -*-
#SEN0482:�������,�����RS485תUARTģ��(DFR0845)��IICת����ģ��(DFR0627)ʹ��

import time
from pinpong.board import Board
from pinpong.libs.rs485winddirection_rs485touart_uarttoi2c import IICSerialWindDirection

Board("uno").begin()  #��ʼ����ѡ����ͺͶ˿ںţ�������˿ں�������Զ�ʶ��

wx = IICSerialWindDirection(IICSerialWindDirection.SUBUART_CHANNEL_1, IA1 = 0, IA0 = 0)

wx.modify_address(0, 2)

while True:
    print(wx.read_wind_direction())
    time.sleep(0.3)