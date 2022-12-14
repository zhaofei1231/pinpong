# -*- coding: utf-8 -*-

import time
import math
from pinpong.board import gboard,I2C

class trim_register:
  def __init__(self):
    self.dig_x1   = 0;
    self.dig_y1   = 0;
    self.dig_x2   = 0;
    self.dig_y2   = 0;
    self.dig_z1   = 0;
    self.dig_z2   = 0;
    self.dig_z3   = 0;
    self.dig_z4   = 0;
    self.dig_xy1  = 0;
    self.dig_xy2  = 0;
    self.dig_xyz1 = 0;
_trim_data = trim_register()

class geomagnetic_data:
  def __init__(self):
    self.x   = 0;
    self.y   = 0;
    self.z   = 0;
    self.r   = 0;
_geomagnetic = geomagnetic_data()

class BMM150(object):
  PI                             = 3.141592653
  I2C_MODE                       = 1
  SPI_MODE                       = 2
  ENABLE_POWER                   = 1
  DISABLE_POWER                  = 0
  POLARITY_HIGH                  = 1
  POLARITY_LOW                   = 0
  ERROR                          = -1
  SELF_TEST_XYZ_FALL             = 0
  SELF_TEST_YZ_FAIL              = 1
  SELF_TEST_XZ_FAIL              = 2
  SELF_TEST_Z_FAIL               = 3
  SELF_TEST_XY_FAIL              = 4
  SELF_TEST_Y_FAIL               = 5
  SELF_TEST_X_FAIL               = 6
  SELF_TEST_XYZ_OK               = 7
  DRDY_ENABLE                    = 1
  DRDY_DISABLE                   = 0
  INTERRUPUT_LATCH_ENABLE        = 1
  INTERRUPUT_LATCH_DISABLE       = 0
  MEASUREMENT_X_ENABLE           = 0
  MEASUREMENT_Y_ENABLE           = 0
  MEASUREMENT_Z_ENABLE           = 0
  MEASUREMENT_X_DISABLE          = 1
  MEASUREMENT_Y_DISABLE          = 1
  MEASUREMENT_Z_DISABLE          = 1
  DATA_OVERRUN_ENABLE            = 1
  DATA_OVERRUN_DISABLE           = 0
  OVERFLOW_INT_ENABLE            = 1
  OVERFLOW_INT_DISABLE           = 0
  INTERRUPT_X_ENABLE             = 0
  INTERRUPT_Y_ENABLE             = 0
  INTERRUPT_Z_ENABLE             = 0
  INTERRUPT_X_DISABLE            = 1
  INTERRUPT_Y_DISABLE            = 1
  INTERRUPT_Z_DISABLE            = 1
  
  CHANNEL_X                      = 1
  CHANNEL_Y                      = 2
  CHANNEL_Z                      = 3
  ENABLE_INTERRUPT_PIN           = 1
  DISABLE_INTERRUPT_PIN          = 0
  POWERMODE_NORMAL               = 0x00
  POWERMODE_FORCED               = 0x01
  POWERMODE_SLEEP                = 0x03
  POWERMODE_SUSPEND              = 0x04
  PRESETMODE_LOWPOWER            = 0x01
  PRESETMODE_REGULAR             = 0x02
  PRESETMODE_HIGHACCURACY        = 0x03
  PRESETMODE_ENHANCED            = 0x04
  REPXY_LOWPOWER                 = 0x01
  REPXY_REGULAR                  = 0x04
  REPXY_ENHANCED                 = 0x07
  REPXY_HIGHACCURACY             = 0x17
  REPZ_LOWPOWER                  = 0x01
  REPZ_REGULAR                   = 0x07
  REPZ_ENHANCED                  = 0x0D
  REPZ_HIGHACCURACY              = 0x29
  CHIP_ID_VALUE                  = 0x32
  CHIP_ID_REGISTER               = 0x40
  REG_DATA_X_LSB                 = 0x42
  REG_DATA_READY_STATUS          = 0x48
  REG_INTERRUPT_STATUS           = 0x4a
  CTRL_POWER_REGISTER            = 0x4b
  MODE_RATE_REGISTER             = 0x4c
  REG_INT_CONFIG                 = 0x4D
  REG_AXES_ENABLE                = 0x4E
  REG_LOW_THRESHOLD              = 0x4F
  REG_HIGH_THRESHOLD             = 0x50
  REG_REP_XY                     = 0x51
  REG_REP_Z                      = 0x52
  RATE_10HZ                      = 0x00        #(default rate)
  RATE_02HZ                      = 0x01
  RATE_06HZ                      = 0x02
  RATE_08HZ                      = 0x03
  RATE_15HZ                      = 0x04
  RATE_20HZ                      = 0x05
  RATE_25HZ                      = 0x06
  RATE_30HZ                      = 0x07
  DIG_X1                         = 0x5D
  DIG_Y1                         = 0x5E
  DIG_Z4_LSB                     = 0x62
  DIG_Z4_MSB                     = 0x63
  DIG_X2                         = 0x64
  DIG_Y2                         = 0x65
  DIG_Z2_LSB                     = 0x68
  DIG_Z2_MSB                     = 0x69
  DIG_Z1_LSB                     = 0x6A
  DIG_Z1_MSB                     = 0x6B
  DIG_XYZ1_LSB                   = 0x6C
  DIG_XYZ1_MSB                   = 0x6D
  DIG_Z3_LSB                     = 0x6E
  DIG_Z3_MSB                     = 0x6F
  DIG_XY2                        = 0x70
  DIG_XY1                        = 0x71
  LOW_THRESHOLD_INTERRUPT        = 0x00
  HIGH_THRESHOLD_INTERRUPT       = 0x01
  NO_DATA                        = -32768
  __txbuf          = [0]          # i2c send buffer
  __threshold_mode = 2

  def __init__(self):
    pass

  '''
    @brief ?????????bmm150 ????????????id????????????
    @return 0  is init success
            -1 is init failed
  '''
  def sensor_init(self):
    self.set_power_bit(self.ENABLE_POWER)
    chip_id = self.get_chip_id()
    if chip_id == self.CHIP_ID_VALUE:
      self.get_trim_data()
      return 0
    else:
      return -1

  '''
    @brief get bmm150 chip id
    @return chip id
  '''
  def get_chip_id(self):
    rslt = self.read_reg(self.CHIP_ID_REGISTER, 1)
    return rslt[0]

  '''
    @brief ????????????????????????????????????????????????????????????????????????????????????,suspend mode?????????????????????
  '''
  def soft_reset(self):
    rslt = self.read_reg(self.CTRL_POWER_REGISTER, 1)
    self.__txbuf[0] = rslt[0] | 0x82
    self.write_reg(self.CTRL_POWER_REGISTER, self.__txbuf)

  '''
    @brief ???????????????????????????????????????????????????
    @return ????????????????????????
  '''
  def self_test(self):
    str1 = ""
    self.set_operation_mode(self.POWERMODE_SLEEP)
    rslt = self.read_reg(self.MODE_RATE_REGISTER, 1)
    self.__txbuf[0] == rslt[0] | 0x01
    self.write_reg(self.MODE_RATE_REGISTER, self.__txbuf)
    time.sleep(1)
    rslt = self.read_reg(self.REG_DATA_X_LSB, 5)
    number = (rslt[0]&0x01) | (rslt[2]&0x01)<<1 | (rslt[4]&0x01)<<2
    if (number>>0)&0x01:
      str1 += "x "
    if (number>>1)&0x01:
      str1 += "y "
    if (number>>2)&0x01:
      str1 += "z "
    if number == 0:
      str1 = "xyz aix self test fail"
    else:
      str1 += "aix test success"
    return str1

  '''
    @brief ?????????????????????
    @param ctrl is enable/disable power
      DISABLE_POWER is disable power
      ENABLE_POWER  is enable power
  '''
  def set_power_bit(self, ctrl):
    rslt = self.read_reg(self.CTRL_POWER_REGISTER, 1)
    if ctrl == self.DISABLE_POWER:
      self.__txbuf[0] = rslt[0] & 0xFE
      self.write_reg(self.CTRL_POWER_REGISTER, self.__txbuf)
    else:
      self.__txbuf[0] = rslt[0] | 0x01
      self.write_reg(self.CTRL_POWER_REGISTER, self.__txbuf)

  '''
    @brief ??????????????????
    @return power state
      DISABLE_POWER is disable power
      ENABLE_POWER  is enable power
  '''
  def get_power_bit(self):
    rslt = self.read_reg(self.CTRL_POWER_REGISTER, 1)
    return rslt[0]&0x01

  '''
    @brief ??????????????????????????????
    @param modes
      POWERMODE_NORMAL       normal mode  ????????????????????????????????????
      POWERMODE_FORCED       forced mode  ????????????????????????????????????????????????sleep mode
      POWERMODE_SLEEP        sleep mode   ????????????????????????????????????????????????????????????
      POWERMODE_SUSPEND      suspend mode ????????????????????????????????? BMM150_REG_POWER_CONTROL?????????
  '''
  def set_operation_mode(self, modes):
    rslt = self.read_reg(self.MODE_RATE_REGISTER, 1)
    if modes == self.POWERMODE_NORMAL:
      self.set_power_bit(self.ENABLE_POWER)
      rslt[0] = rslt[0] & 0xf9
      self.write_reg(self.MODE_RATE_REGISTER, rslt)
    elif modes == self.POWERMODE_FORCED:
      rslt[0] = (rslt[0] & 0xf9) | 0x02
      self.set_power_bit(self.ENABLE_POWER)
      self.write_reg(self.MODE_RATE_REGISTER, rslt)
    elif modes == self.POWERMODE_SLEEP:
      self.set_power_bit(self.ENABLE_POWER)
      rslt[0] = (rslt[0] & 0xf9) | 0x04
      self.write_reg(self.MODE_RATE_REGISTER, rslt)
    else:
      self.set_power_bit(self.DISABLE_POWER)

  '''
    @brief ??????????????????????????????
    @return ????????????????????????
  '''
  def get_operation_mode(self):
    str1 = ""
    if self.get_power_bit() == 0:
      mode = self.POWERMODE_SUSPEND
    else:
      rslt = self.read_reg(self.MODE_RATE_REGISTER, 1)
      mode = (rslt[0]&0x06)>>1
    if mode == self.POWERMODE_NORMAL:
      str1 = "normal mode"
    elif mode == self.POWERMODE_SLEEP:
      str1 = "sleep mode"
    elif mode == self.POWERMODE_SUSPEND:
      str1 = "suspend mode"
    else:
      str1 = "forced mode"
    return str1

  '''
    @brief ????????????????????????????????????????????????????????????(??????????????????)
    @param rate
      RATE_02HZ
      RATE_06HZ
      RATE_08HZ
      RATE_10HZ        #(default rate)
      RATE_15HZ
      RATE_20HZ
      RATE_25HZ
      RATE_30HZ
  '''
  def set_rate(self, rates):
    rslt = self.read_reg(self.MODE_RATE_REGISTER, 1)
    if rates == self.RATE_10HZ:
      rslt[0] = rslt[0]&0xc7
      self.write_reg(self.MODE_RATE_REGISTER, rslt)
    elif rates == self.RATE_02HZ:
      rslt[0] = (rslt[0]&0xc7) | 0x08
      self.write_reg(MODE_RATE_REGISTER, rslt)
    elif rates == self.RATE_06HZ:
      rslt[0] = (rslt[0]&0xc7) | 0x10
      self.write_reg(MODE_RATE_REGISTER, rslt)
    elif rates == self.RATE_08HZ:
      rslt[0] = (rslt[0]&0xc7) | 0x18
      self.write_reg(self.MODE_RATE_REGISTER, rslt)
    elif rates == self.RATE_15HZ:
      rslt[0] = (rslt[0]&0xc7) | 0x20
      self.write_reg(self.MODE_RATE_REGISTER, rslt)
    elif rates == RATE_20HZ:
      rslt[0] = (rslt[0]&0xc7) | 0x28
      self.write_reg(self.MODE_RATE_REGISTER, rslt)
    elif rates == self.RATE_25HZ:
      rslt[0] = (rslt[0]&0xc7) | 0x30
      self.write_reg(MODE_RATE_REGISTER, rslt)
    elif rates == self.RATE_30HZ:
      rslt[0] = (rslt[0]&0xc7) | 0x38
      self.write_reg(self.MODE_RATE_REGISTER, rslt)
    else:
      rslt[0] = rslt[0]&0xc7
      self.write_reg(self.MODE_RATE_REGISTER, rslt)

  '''
    @brief ??????????????????????????? ?????????HZ
    @return rate
  '''
  def get_rate(self):
    rslt = self.read_reg(self.MODE_RATE_REGISTER, 1)
    rate = (rslt[0]&0x38)>>3
    if rate == self.RATE_02HZ:
      return 2
    elif rate == self.RATE_06HZ:
      return 6
    elif rate == self.RATE_08HZ:
      return 8
    elif rate == self.RATE_10HZ:
      return 10
    elif rate == self.RATE_15HZ:
      return 15
    elif rate == self.RATE_20HZ:
      return 20
    elif rate == self.RATE_25HZ:
      return 25
    else:
      return 30

  '''
    @brief ??????????????????????????????????????????????????????????????????????????????
    @param modes 
       PRESETMODE_LOWPOWER       ???????????????,????????????????????? ?????????
       PRESETMODE_REGULAR        ????????????,?????????????????? ?????????
       PRESETMODE_ENHANCED       ????????????,?????????????????? ?????????
       PRESETMODE_HIGHACCURACY   ???????????????,????????????????????? ?????????
  '''
  def set_preset_mode(self, modes):
    if modes == self.PRESETMODE_LOWPOWER:
      self.set_xy_rep(self.REPXY_LOWPOWER)
      self.set_z_rep(self.REPZ_LOWPOWER)
    elif modes == self.PRESETMODE_REGULAR:
      self.set_xy_rep(self.REPXY_REGULAR)
      self.set_z_rep(self.REPZ_REGULAR)
    elif modes == self.PRESETMODE_HIGHACCURACY:
      self.set_xy_rep(self.REPXY_HIGHACCURACY)
      self.set_z_rep(self.REPZ_HIGHACCURACY)
    elif modes == self.PRESETMODE_ENHANCED:
      self.set_xy_rep(self.REPXY_ENHANCED)
      self.set_z_rep(self.REPZ_ENHANCED)
    else:
      self.set_xy_rep(self.REPXY_LOWPOWER)
      self.set_z_rep(self.REPZ_LOWPOWER)

  '''
    @brief the number of repetitions for x/y-axis
    @param modes
      PRESETMODE_LOWPOWER      ???????????????????????????????????????????????????
      PRESETMODE_REGULAR       ??????????????????????????????????????????
      PRESETMODE_HIGHACCURACY  ??????????????????????????????????????????
      PRESETMODE_ENHANCED      ??????????????????????????????????????????????????????
  '''
  def set_xy_rep(self, modes):
    self.__txbuf[0] = modes
    if modes == self.REPXY_LOWPOWER:
      self.write_reg(self.REG_REP_XY, self.__txbuf)
    elif modes == self.REPXY_REGULAR:
      self.write_reg(self.REG_REP_XY, self.__txbuf)
    elif modes == self.REPXY_ENHANCED:
      self.write_reg(self.REG_REP_XY, self.__txbuf)
    elif modes == self.REPXY_HIGHACCURACY:
      self.write_reg(self.REG_REP_XY, self.__txbuf)
    else:
      __txbuf[0] = self.REPXY_LOWPOWER
      self.write_reg(self.REG_REP_XY, self.__txbuf)

  '''
    @brief the number of repetitions for z-axis
    @param modes
      PRESETMODE_LOWPOWER      ???????????????????????????????????????????????????
      PRESETMODE_REGULAR       ??????????????????????????????????????????
      PRESETMODE_HIGHACCURACY  ??????????????????????????????????????????
      PRESETMODE_ENHANCED      ??????????????????????????????????????????????????????
  '''
  def set_z_rep(self, modes):
    self.__txbuf[0] = modes
    if modes == self.REPZ_LOWPOWER:  
      self.write_reg(self.REG_REP_Z, self.__txbuf)
    elif modes == self.REPZ_REGULAR:
      self.write_reg(self.REG_REP_Z, self.__txbuf)
    elif modes == self.REPZ_ENHANCED:
      self.write_reg(self.REG_REP_Z, self.__txbuf)
    elif modes == self.REPZ_HIGHACCURACY:
      self.write_reg(self.REG_REP_Z, self.__txbuf)
    else:
      __txbuf[0] = self.REPZ_LOWPOWER
      self.write_reg(self.REG_REP_Z, self.__txbuf)

  '''
    @brief ??????bmm150?????????????????????????????????????????????????????????
  '''
  def get_trim_data(self):
    trim_x1_y1    = self.read_reg(self.DIG_X1, 2)
    trim_xyz_data = self.read_reg(self.DIG_Z4_LSB, 4)
    trim_xy1_xy2  = self.read_reg(self.DIG_Z2_LSB, 10)
    _trim_data.dig_x1 = self.uint8_to_int8(trim_x1_y1[0])
    _trim_data.dig_y1 = self.uint8_to_int8(trim_x1_y1[1])
    _trim_data.dig_x2 = self.uint8_to_int8(trim_xyz_data[2])
    _trim_data.dig_y2 = self.uint8_to_int8(trim_xyz_data[3])
    temp_msb = int(trim_xy1_xy2[3]) << 8
    _trim_data.dig_z1 = int(temp_msb | trim_xy1_xy2[2])
    temp_msb = int(trim_xy1_xy2[1] << 8)
    _trim_data.dig_z2 = int(temp_msb | trim_xy1_xy2[0])
    temp_msb = int(trim_xy1_xy2[7] << 8)
    _trim_data.dig_z3 = temp_msb | trim_xy1_xy2[6]
    temp_msb = int(trim_xyz_data[1] << 8)
    _trim_data.dig_z4 = int(temp_msb | trim_xyz_data[0])
    _trim_data.dig_xy1 = trim_xy1_xy2[9]
    _trim_data.dig_xy2 = self.uint8_to_int8(trim_xy1_xy2[8])
    temp_msb = int((trim_xy1_xy2[5] & 0x7F) << 8)
    _trim_data.dig_xyz1 = int(temp_msb | trim_xy1_xy2[4])

  '''
    @brief ??????x y z ?????????????????????
    @return x y z ?????????????????????????????? ????????????????????????uT???
            [0] x ??????????????????
            [1] y ??????????????????
            [2] z ??????????????????
  '''
  def get_geomagnetic(self):
    rslt = self.read_reg(self.REG_DATA_X_LSB, 8)
    rslt[1] = self.uint8_to_int8(rslt[1])
    rslt[3] = self.uint8_to_int8(rslt[3])
    rslt[5] = self.uint8_to_int8(rslt[5])
    _geomagnetic.x = ((rslt[0]&0xF8) >> 3)  | int(rslt[1]*32)
    _geomagnetic.y = ((rslt[2]&0xF8) >> 3)  | int(rslt[3]*32)
    _geomagnetic.z = ((rslt[4]&0xFE) >> 1)  | int(rslt[5]*128)
    _geomagnetic.r = ((rslt[6]&0xFC) >> 2)  | int(rslt[7]*64)
    rslt[0] = self.compenstate_x(_geomagnetic.x, _geomagnetic.r)
    rslt[1] = self.compenstate_y(_geomagnetic.y, _geomagnetic.r)
    rslt[2] = self.compenstate_z(_geomagnetic.z, _geomagnetic.r)
    return rslt

  '''
    @brief ??????????????????
    @return ???????????? (0?? - 360??)  0?? = North, 90?? = East, 180?? = South, 270?? = West.
  '''
  def get_compass_degree(self):
    geomagnetic = self.get_geomagnetic()
    compass = math.atan2(geomagnetic[0], geomagnetic[1])
    if compass < 0:
      compass += 2 * self.PI
    if compass > 2 * self.PI:
     compass -= 2 * self.PI
    return compass * 180 / self.PI

  '''
    @brief uint8_t to int8_t
    @param number    ???????????????uint8_t??????
    @return number   ??????????????????
  '''
  def uint8_to_int8(self, number):
    if number <= 127:
      return number
    else:
      return (256-number)*-1

  '''
    @berif ??????x??????????????????
    @param  data_x       ?????????????????????
    @param  data_r       ???????????????
    @return retval       ????????????????????????
  '''
  def compenstate_x(self, data_x, data_r):
    if data_x != -4096:
      if data_r != 0:
        process_comp_x0 = data_r
      elif _trim_data.dig_xyz1 != 0:
        process_comp_x0 = _trim_data.dig_xyz1
      else:
        process_comp_x0 = 0
      if process_comp_x0 != 0:
        process_comp_x1 = int(_trim_data.dig_xyz1*16384)
        process_comp_x2 = int(process_comp_x1/process_comp_x0 - 0x4000)
        retval = process_comp_x2
        process_comp_x3 = retval*retval
        process_comp_x4 = _trim_data.dig_xy2*(process_comp_x3/128)
        process_comp_x5 = _trim_data.dig_xy1*128
        process_comp_x6 = retval*process_comp_x5
        process_comp_x7 = (process_comp_x4+process_comp_x6)/512 + 0x100000
        process_comp_x8 = _trim_data.dig_x2 + 0xA0
        process_comp_x9 = (process_comp_x8*process_comp_x7)/4096
        process_comp_x10= data_x*process_comp_x9
        retval = process_comp_x10/8192
        retval = (retval + _trim_data.dig_x1*8)/16
      else:
        retval = -32368
    else:
      retval = -32768
    return retval

  '''
    @berif ??????y??????????????????
    @param  data_y       ?????????????????????
    @param  data_r       ???????????????
    @return retval       ????????????????????????
  '''
  def compenstate_y(self, data_y, data_r):
    if data_y != -4096:
      if data_r != 0:
        process_comp_y0 = data_r
      elif _trim_data.dig_xyz1 != 0:
        process_comp_y0 = _trim_data.dig_xyz1
      else:
        process_comp_y0 = 0
      if process_comp_y0 != 0:
        process_comp_y1 = int(_trim_data.dig_xyz1*16384/process_comp_y0)
        process_comp_y2 = int(process_comp_y1 - 0x4000)
        retval = process_comp_y2
        process_comp_y3 = retval*retval
        process_comp_y4 = _trim_data.dig_xy2*(process_comp_y3/128)
        process_comp_y5 = _trim_data.dig_xy1*128
        process_comp_y6 = (process_comp_y4+process_comp_y5*retval)/512
        process_comp_y7 = _trim_data.dig_y2 + 0xA0
        process_comp_y8 = ((process_comp_y6 + 0x100000)*process_comp_y7)/4096
        process_comp_y9 = data_y*process_comp_y8
        retval = process_comp_y9/8192
        retval = (retval + _trim_data.dig_y1*8)/16
      else:
        retval = -32368
    else:
      retval = -32768
    return retval

  '''
    @berif ??????z??????????????????
    @param  data_z       ?????????????????????
    @param  data_r       ???????????????
    @return retval       ????????????????????????
  '''
  def compenstate_z(self, data_z, data_r):
    if data_z != -16348:
      if _trim_data.dig_z2 != 0 and _trim_data.dig_z1 != 0 and _trim_data.dig_xyz1 != 0 and data_r != 0:
        process_comp_z0 = data_r - _trim_data.dig_xyz1
        process_comp_z1 = (_trim_data.dig_z3*process_comp_z0)/4
        process_comp_z2 = (data_z - _trim_data.dig_z4)*32768
        process_comp_z3 = _trim_data.dig_z1 * data_r*2
        process_comp_z4 = (process_comp_z3+32768)/65536
        retval = (process_comp_z2 - process_comp_z1)/(_trim_data.dig_z2+process_comp_z4)
        if retval > 32767:
          retval = 32367
        elif retval < -32367:
          retval = -32367
        retval = retval/16
      else:
        retval = -32768
    else:
      retval = -32768
    return retval

  '''
    @brief ??????????????????????????????????????????
           ????????????????????????DRDY????????????
           ????????????????????????DRDY???????????????
           ??????????????????????????????????????????????????????????????????????????????????????????
           ??????????????????????????????????????????????????????????????????????????????????????????
    @param modes
        DRDY_ENABLE      ??????DRDY
        DRDY_DISABLE     ??????DRDY
    @param polarity
        POLARITY_HIGH    ?????????
        POLARITY_LOW     ?????????
  '''
  def set_data_ready_pin(self, modes, polarity):
    rslt = self.read_reg(self.REG_AXES_ENABLE, 1)
    if modes == self.DRDY_DISABLE:
      self.__txbuf[0] = rslt[0] & 0x7F
    else:
      self.__txbuf[0] = rslt[0] | 0x80
    if polarity == self.POLARITY_LOW:
      self.__txbuf[0] = self.__txbuf[0] & 0xFB
    else:
      self.__txbuf[0] = self.__txbuf[0] | 0x04
    self.write_reg(self.REG_AXES_ENABLE, self.__txbuf)

  '''
    @brief ???????????????????????????????????????????????????????????????
    @return status
      1 is   data is ready
      0 is   data is not ready
  '''
  def get_data_ready_state(self):
    rslt = self.read_reg(self.REG_DATA_READY_STATUS, 1)
    if (rslt[0]&0x01) != 0:
      return 1
    else:
      return 0

  '''
    @brief ??????x y z ???????????????????????????????????????????????????????????????xyz???????????????????????????
    @param channel_x
      MEASUREMENT_X_ENABLE     ?????? x ????????????
      MEASUREMENT_X_DISABLE    ?????? x ????????????
    @param channel_y
      MEASUREMENT_Y_ENABLE     ?????? y ????????????
      MEASUREMENT_Y_DISABLE    ?????? y ????????????
    @param channel_z
      MEASUREMENT_Z_ENABLE     ?????? z ????????????
      MEASUREMENT_Z_DISABLE    ?????? z ????????????
  '''
  def set_measurement_xyz(self, channel_x = MEASUREMENT_X_ENABLE, channel_y = MEASUREMENT_Y_ENABLE, channel_z = MEASUREMENT_Z_ENABLE):
    rslt = self.read_reg(self.REG_AXES_ENABLE, 1)
    if channel_x == self.MEASUREMENT_X_DISABLE:
      self.__txbuf[0] = rslt[0] | 0x08
    else:
      self.__txbuf[0] = rslt[0] & 0xF7

    if channel_y == self.MEASUREMENT_Y_DISABLE:
      self.__txbuf[0] = self.__txbuf[0] | 0x10
    else:
      self.__txbuf[0] = self.__txbuf[0] & 0xEF

    if channel_z == self.MEASUREMENT_Z_DISABLE:
      self.__txbuf[0] = self.__txbuf[0] | 0x20
    else:
      self.__txbuf[0] = self.__txbuf[0] & 0xDF
    self.write_reg(self.REG_AXES_ENABLE, self.__txbuf)

  '''
    @brief ?????? x y z ??????????????????
    @return ??????xyz ??????????????????????????????
  '''
  def get_measurement_xyz_state(self):
    str1 = ""
    rslt = self.read_reg(self.REG_AXES_ENABLE, 1)
    if (rslt[0]&0x08) == 0:
      str1 += "x "
    if (rslt[0]&0x10) == 0:
      str1 += "y "
    if (rslt[0]&0x20) == 0:
      str1 += "z "
    if str1 == "":
      str1 = "xyz aix not enable"
    else:
      str1 += "aix enable"
    return str1

  '''
    @brief ?????????????????? INT ????????????
           ???????????????????????????????????? INT ???????????????
           ??????????????? INT ???????????????????????????????????????
           ??????????????????????????????????????????????????????????????????????????????????????????
           ??????????????????????????????????????????????????????????????????????????????????????????
    @param modes
      ENABLE_INTERRUPT_PIN     ??????????????????
      DISABLE_INTERRUPT_PIN    ??????????????????
    @param polarity
      POLARITY_HIGH            ?????????
      POLARITY_LOW             ?????????
  '''
  def set_interrupt_pin(self, modes, polarity):
    rslt = self.read_reg(self.REG_AXES_ENABLE, 1)
    if modes == self.DISABLE_INTERRUPT_PIN:
      self.__txbuf[0] = rslt[0] & 0xBF
    else:
      self.__txbuf[0] = rslt[0] | 0x40
    if polarity == self.POLARITY_LOW:
      self.__txbuf[0] = self.__txbuf[0] & 0xFE
    else:
      self.__txbuf[0] = self.__txbuf[0] | 0x01
    self.write_reg(self.REG_AXES_ENABLE, self.__txbuf)

  '''
    @brief ?????????????????????????????????????????????????????? BMM150_REG_INTERRUPT_STATUS ??????????????????????????????????????????
                             ????????????????????????????????????
    @param modes
      INTERRUPUT_LATCH_ENABLE         ????????????
      INTERRUPUT_LATCH_DISABLE        ???????????????
  '''
  def set_interruput_latch(self, modes):
    rslt = self.read_reg(self.REG_AXES_ENABLE, 1)
    if modes == self.INTERRUPUT_LATCH_DISABLE:
      self.__txbuf[0] = rslt[0] & 0xFD
    else:
      self.__txbuf[0] = rslt[0] | 0x02
    self.write_reg(self.REG_AXES_ENABLE, self.__txbuf)

  '''
    @brief ???????????????????????????????????????????????????/???????????????????????????
           ??????????????????????????????????????????????????????????????????????????????????????????
           ??????????????????????????????????????????????????????????????????????????????????????????
    @param modes
      LOW_THRESHOLD_INTERRUPT     ?????????????????????
      HIGH_THRESHOLD_INTERRUPT    ?????????????????????
    @param threshold
      ?????????????????????16?????????????????????????????????????????????1???????????????16?????????????????????????????????
    @param polarity
      POLARITY_HIGH               ?????????
      POLARITY_LOW                ?????????
    @param channelX
      INTERRUPT_X_ENABLE          ?????? x ??????????????????
      INTERRUPT_X_DISABLE         ?????? x ??????????????????
    @param channelY
      INTERRUPT_Y_ENABLE          ?????? y ??????????????????
      INTERRUPT_Y_DISABLE         ?????? y ??????????????????
    @param channelZ
      INTERRUPT_Z_ENABLE          ?????? z ??????????????????
      INTERRUPT_Z_DISABLE         ?????? z ??????????????????
  '''
  def set_threshold_interrupt(self, mode, threshold, polarity, channel_x = INTERRUPT_X_ENABLE, channel_y = INTERRUPT_Y_ENABLE, channel_z = INTERRUPT_Z_ENABLE):
    if mode == self.LOW_THRESHOLD_INTERRUPT:
      self.__threshold_mode = self.LOW_THRESHOLD_INTERRUPT
      self.set_low_threshold_interrupt(channel_x, channel_y, channel_z, threshold, polarity)
    else:
      self.__threshold_mode = self.HIGH_THRESHOLD_INTERRUPT
      self.set_high_threshold_interrupt(channel_x, channel_y, channel_z, threshold, polarity)

  '''
    @brief ?????????????????????????????????
    @return ???????????????????????????????????????????????????????????????????????????
            [0] x ???????????????????????? ???????????????NO_DATA??????????????????
            [1] y ???????????????????????? ???????????????NO_DATA??????????????????
            [2] z ???????????????????????? ???????????????NO_DATA??????????????????
            [3] ??????????????????????????????????????????
            [4] ????????????????????????????????????????????????????????????
               bit0 is 1 ??????x????????????????????????
               bit1 is 1 ??????y????????????????????????
               bit2 is 1 ??????z????????????????????????
               ------------------------------------
               | bit7 ~ bit3 | bit2 | bit1 | bit0 |
               ------------------------------------
               |  reserved   |  0   |  0   |  0   |
               ------------------------------------
  '''
  def get_threshold_interrupt_data(self):
    data = [0]*10
    str1 = ""
    if self.__threshold_mode == self.LOW_THRESHOLD_INTERRUPT:
      state = self.get_low_threshold_interrupt_state()
    else:
      state = self.get_high_threshold_interrupt_state()
    rslt = self.get_geomagnetic()
    if (state>>0)&0x01:
      data[0] = rslt[0]
      str1 += "X "
    else:
      data[0] = self.NO_DATA
    if (state>>1)&0x01:
      data[1] = rslt[1]
      str1 += "Y "
    else:
      data[1] = self.NO_DATA
    if (state>>2)&0x01:
      data[2] = rslt[2]
      str1 += "Z "
    else:
      data[2] = self.NO_DATA
    if state != 0:
      str1 += " threshold interrupt"
    data[3] = str1
    data[4] = state&0x07
    
    return data
  '''
    @brief ?????????????????????????????????????????????????????????????????????????????????
           ??????????????????????????????????????????????????????????????????????????????????????????
           ??????????????????????????????????????????????????????????????????????????????????????????
    @param channelX
      INTERRUPT_X_ENABLE          ?????? x ??????????????????
      INTERRUPT_X_DISABLE         ?????? x ??????????????????
    @param channelY
      INTERRUPT_Y_ENABLE          ?????? y ??????????????????
      INTERRUPT_Y_DISABLE         ?????? y ??????????????????
    @param channelZ
      INTERRUPT_Z_ENABLE          ?????? z ??????????????????
      INTERRUPT_Z_DISABLE         ?????? z ??????????????????
    @param low_threshold              ????????????????????????16????????????????????? 1 ????????????????????????16?????????????????????????????????
    @param polarity
      POLARITY_HIGH                   ?????????
      POLARITY_LOW                    ?????????
  '''
  def set_low_threshold_interrupt(self, channel_x, channel_y, channel_z, low_threshold, polarity):
    if low_threshold < 0:
      self.__txbuf[0] = (low_threshold*-1) | 0x80
    else:
      self.__txbuf[0] = low_threshold
    self.write_reg(REG_LOW_THRESHOLD ,self.__txbuf)
    rslt = self.read_reg(REG_INT_CONFIG, 1)
    if channel_x == self.INTERRUPT_X_DISABLE:
      self.__txbuf[0] = rslt[0] | 0x01
    else:
      self.__txbuf[0] = rslt[0] & 0xFE
    if channel_y == self.INTERRUPT_Y_DISABLE:
      self.__txbuf[0] = self.__txbuf[0] | 0x02
    else:
      self.__txbuf[0] = self.__txbuf[0] & 0xFC
    if channel_x == self.INTERRUPT_X_DISABLE:
      self.__txbuf[0] = self.__txbuf[0] | 0x04
    else:
      self.__txbuf[0] = self.__txbuf[0] & 0xFB
    self.write_reg(self.REG_INT_CONFIG ,self.__txbuf)
    self.set_interrupt_pin(self.ENABLE_INTERRUPT_PIN, polarity)

  '''
    @brief ??????????????????????????????????????????????????????????????????
    @return status ??????????????????????????????????????????????????????
        bit0 is 1 ??????x??????????????????
        bit1 is 1 ??????y??????????????????
        bit2 is 1 ??????z??????????????????
          ------------------------------------
          | bit7 ~ bit3 | bit2 | bit1 | bit0 |
          ------------------------------------
          |  reserved   |  0   |  0   |  0   |
          ------------------------------------
  '''
  def get_low_threshold_interrupt_state(self):
    rslt = self.read_reg(self.REG_INTERRUPT_STATUS, 1)
    return rslt[0]&0x07

  '''
    @brief??????????????????????????????????????????????????????????????????????????????????????????????????????16???
         INT ???????????????????????????????????????
         ?????????????????????????????????????????????????????????????????????????????????????????????????????????
         ?????????????????????????????????????????????????????????????????????????????????????????????????????????
    @param channelX
      INTERRUPT_X_ENABLE          ?????? x ??????????????????
      INTERRUPT_X_DISABLE         ?????? x ??????????????????
    @param channelY
      INTERRUPT_Y_ENABLE          ?????? y ??????????????????
      INTERRUPT_Y_DISABLE         ?????? y ??????????????????
    @param channelZ
      INTERRUPT_Z_ENABLE          ?????? z ??????????????????
      INTERRUPT_Z_DISABLE         ?????? z ??????????????????
    @param high_threshold              ????????????????????????16????????????????????? 1 ????????????????????????16?????????????????????????????????
    @param polarity
      POLARITY_HIGH                   ?????????
      POLARITY_LOW                    ?????????
  '''
  def set_high_threshold_interrupt(self, channel_x, channel_y, channel_z, high_threshold, polarity):
    if high_threshold < 0:
      self.__txbuf[0] = (high_threshold*-1) | 0x80
    else:
      self.__txbuf[0] = high_threshold
    self.write_reg(self.REG_HIGH_THRESHOLD, self.__txbuf)
    rslt = self.read_reg(self.REG_INT_CONFIG, 1)
    if channel_x == self.HIGH_INTERRUPT_X_DISABLE:
      self.__txbuf[0] = rslt[0] | 0x08
    else:
      self.__txbuf[0] = rslt[0] & 0xF7
    if channel_y == self.HIGH_INTERRUPT_Y_DISABLE:
      self.__txbuf[0] = self.__txbuf[0] | 0x10
    else:
      self.__txbuf[0] = self.__txbuf[0] & 0xEF
    if channel_x == self.HIGH_INTERRUPT_X_DISABLE:
      self.__txbuf[0] = self.__txbuf[0] | 0x20
    else:
      self.__txbuf[0] = self.__txbuf[0] & 0xDf    
    
    self.write_reg(REG_INT_CONFIG ,self.__txbuf)
    self.set_interrupt_pin(ENABLE_INTERRUPT_PIN, polarity)

  '''
    @brief ??????????????????????????????????????????????????????????????????
    @return status  ??????????????????????????????????????????????????????
      bit0 is 1 ??????x??????????????????
      bit1 is 1 ??????y??????????????????
      bit2 is 1 ??????z??????????????????
        ------------------------------------
        | bit7 ~ bit3 | bit2 | bit1 | bit0 |
        ------------------------------------
        |  reserved   |  0   |  0   |  0   |
        ------------------------------------
  '''
  def get_high_threshold_interrupt_state(self):
    rslt = self.read_reg(self.REG_INTERRUPT_STATUS, 1)
    return (rslt[0]&0x38)>>3

'''
  @brief An example of an i2c interface module
'''
class BMM150_I2C(BMM150):
  def __init__(self, i2c_addr = 0x13, bus_num = 1 ):
    self.__addr = i2c_addr
    self.i2c = I2C(bus_num)
    super(BMM150_I2C, self).__init__()

  '''
    @brief writes data to a register
    @param reg register address
    @param value written data
  '''
  def write_reg(self, reg, data):
    while 1:
      try:
        self.i2c.writeto_mem(self.__addr, reg, data)
        return
      except Exception:
        print("please check connect!")
        #os.system('i2cdetect -y 1')
        time.sleep(1)
        return
  '''
    @brief read the data from the register
    @param reg register address
    @param value read data
  '''
  def read_reg(self, reg ,len):
    while 1:
      try:
        rslt = self.i2c.readfrom_mem(self.__addr, reg, len)
        #print rslt
        return rslt
      except Exception:
        time.sleep(1)
        print("please check connect!")