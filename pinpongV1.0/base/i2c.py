# -*- coding: utf-8 -*-
import sys
from contextlib import closing
import posix
from fcntl import ioctl
#from i2c_ctypes import *
#from pinpong.base.i2c_ctypes import *
from ctypes import create_string_buffer, sizeof, c_int, byref, pointer, addressof, string_at


assert sys.version_info.major >= 3, __name__ + " is only supported on Python 3"


from ctypes import c_int, c_uint16, c_ushort, c_short, c_ubyte, c_char, POINTER, Structure

# /usr/include/linux/i2c-dev.h: 38
class i2c_msg(Structure):
    """<linux/i2c-dev.h> struct i2c_msg"""
    
    _fields_ = [
        ('addr', c_uint16),
        ('flags', c_ushort),
        ('len', c_short),
        ('buf', POINTER(c_char))]
    
    __slots__ = [name for name,type in _fields_]




# i2c_msg flags
I2C_M_TEN		= 0x0010	# this is a ten bit chip address
I2C_M_RD		= 0x0001	# read data, from slave to master
I2C_M_NOSTART		= 0x4000	# if I2C_FUNC_PROTOCOL_MANGLING
I2C_M_REV_DIR_ADDR	= 0x2000	# if I2C_FUNC_PROTOCOL_MANGLING
I2C_M_IGNORE_NAK	= 0x1000	# if I2C_FUNC_PROTOCOL_MANGLING
I2C_M_NO_RD_ACK		= 0x0800	# if I2C_FUNC_PROTOCOL_MANGLING
I2C_M_RECV_LEN		= 0x0400	# length will be first received byte


# /usr/include/linux/i2c-dev.h: 155
class i2c_rdwr_ioctl_data(Structure):
    """<linux/i2c-dev.h> struct i2c_rdwr_ioctl_data"""
    _fields_ = [
        ('msgs', POINTER(i2c_msg)),
        ('nmsgs', c_int)]

    __slots__ = [name for name,type in _fields_]

I2C_FUNC_I2C			= 0x00000001
I2C_FUNC_10BIT_ADDR		= 0x00000002
I2C_FUNC_PROTOCOL_MANGLING	= 0x00000004 # I2C_M_NOSTART etc.


# ioctls

I2C_SLAVE	= 0x0703	# Change slave address			
				# Attn.: Slave address is 7 or 10 bits  
I2C_SLAVE_FORCE	= 0x0706	# Change slave address			
				# Attn.: Slave address is 7 or 10 bits  
				# This changes the address, even if it  
				# is already taken!			
I2C_TENBIT	= 0x0704	# 0 for 7 bit addrs, != 0 for 10 bit	
I2C_FUNCS	= 0x0705	# Get the adapter functionality         
I2C_RDWR	= 0x0707	# Combined R/W transfer (one stop only) 


class I2CMaster(object):
    
    def __init__(self, n, extra_open_flags=0):
        
        self.fd = posix.open("/dev/i2c-%i"%n, posix.O_RDWR|extra_open_flags)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
    
    def close(self):
        posix.close(self.fd)
    
    def transaction(self, *msgs):
        #print("tuple",msgs[0].addr, msgs[0].flags, msgs[0].len, msgs[0].buf[0])
        msg_count = len(msgs)
        msg_array = (i2c_msg*msg_count)(*msgs)
        ioctl_arg = i2c_rdwr_ioctl_data(msgs=msg_array, nmsgs=msg_count)
        ioctl(self.fd, I2C_RDWR, ioctl_arg)
        
        return [i2c_msg_to_bytes(m) for m in msgs if (m.flags & I2C_M_RD)]

def reading(addr, n_bytes):

    buf = create_string_buffer(n_bytes)
    return i2c_msg(addr=addr, flags=I2C_M_RD, len=sizeof(buf), buf=buf)


def writing(addr, byte_seq):

    byte_seq = tuple(byte_seq)
    buf = bytes(byte_seq)
    buf = create_string_buffer(buf,len(buf))
    a = i2c_msg(addr=addr, flags=0, len=sizeof(buf), buf=buf)
    return a

def i2c_msg_to_bytes(m):
    return string_at(m.buf, m.len)
