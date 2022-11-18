# -*- coding: utf-8 -*-
#SEN0483:���ٲ���,�����RS485תUARTģ��(DFR0845)��IICת����ģ��(DFR0627)ʹ��

import time
from pinpong.board import Board
from pinpong.libs.rs485windspeed_rs485touart_uarttoi2c import IICSerialWindSpeed

Board("UNIHIKER").begin()  #��ʼ����ѡ����ͺͶ˿ںţ�������˿ں�������Զ�ʶ��

ws = IICSerialWindSpeed(IICSerialWindSpeed.SUBUART_CHANNEL_1, IA1 = 0, IA0 = 0)

ws.modify_address(0, 2)
while True:
    print(ws.read_wind_speed())
    time.sleep(0.3)