# -*- coding: utf-8 -*- 
from comm import Meg

def PINPONGinit():
  Meg[boardname] = "UNO"
  Meg[connecte] = False
  Meg[spi_wifi_uno] = True
  Meg[firm] = "/base/FirmataExpress.UNO_PB."
  return Meg
  
