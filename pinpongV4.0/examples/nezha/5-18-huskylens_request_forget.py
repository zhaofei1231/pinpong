# -*- coding: utf-8 -*-

#NeZha
#实验效果：触发遗忘功能

import time
from pinpong.board import Board
from pinpong.libs.dfrobot_huskylens import Huskylens

Board("nezha").begin()

husky = Huskylens()


#husky.command_request_knock()
#       Header	Header 2	Address	  Data Length	Command	 Checksum
#return 0x55	0xAA	    0x11	      0x00	    0x2E	 0x3E


husky.command_request_forget()
time.sleep(2)





