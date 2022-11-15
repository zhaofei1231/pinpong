# -*- coding: utf-8 -*-

import time
i=0
if i == 1:
  raise ValueError("错误")
else:
  raise ValueError("异常")
  
while True:
  print(i)
  time.sleep(1)