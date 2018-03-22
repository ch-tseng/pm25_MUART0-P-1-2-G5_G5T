#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial
import time
import sys
import base64

#Usage
#  air=G3(baudrate=9600)
#  pmdata = (air.read("/dev/ttyS0"))
#  print (pmdata[3], pmdata[4], pmdata[5])

class G5():
    def __init__(self, debug=False):
        if debug: print ("init")
        self.endian = sys.byteorder
        self.debug = debug

    def conn_serial_port(self, device):
        if self.debug: print (device)
        self.serial = serial.Serial(device, baudrate=9600, timeout= 0.5)
        if self.debug: print ("conn ok")

    def check_keyword(self):
        if self.debug: print ("check_keyword")
        while True:
            token = self.serial.read()
            #token_hex=token.encode('hex')
            token_hex = token.hex()
            if self.debug: print (token_hex)
            if token_hex == '42':
                if self.debug: print ("get 42")
                token2 = self.serial.read()
                #token2_hex=token2.encode('hex')
                token2_hex = token2.hex()
                if self.debug: print (token2_hex)
                if token2_hex == '4d':
                    if self.debug: print ("get 4d")
                    return True
                elif token2_hex == '00': # fixme
                    if self.debug: print ("get 00")
                    token3 = self.serial.read()
                    #token3_hex=token3.encode('hex')
                    token3_hex = token3.hex()
                    if token3_hex == '4d':
                        if self.debug: print ("get 4d")
                        return True

    def vertify_data(self, data):
        if self.debug: print ("teset:"+data)
        n = 2
        sum = int('42',16)+int('4d',16)
        for i in range(0, len(data)-4, n):
            #print data[i:i+n]
            sum=sum+int(data[i:i+n],16)
        try:
            versum = int(data[40]+data[41]+data[42]+data[43],16)
        except:
            versum = 0

        if self.debug: print (sum)
        if self.debug: print (versum)
        #if sum == versum:

    def read_data(self):
        data = self.serial.read(32)
        #data_hex=data.encode('hex')
        #print("read_data...2")
        data_hex = data.hex()
        #print("read_data...3")
        #print("len:", len(data_hex), data_hex)
        if self.debug: self.vertify_data(data_hex)
        try: 
            pm1_cf=int(data_hex[4]+data_hex[5]+data_hex[6]+data_hex[7],16) 
        except: 
            pm1_cf=0
        try: 
            pm25_cf=int(data_hex[8]+data_hex[9]+data_hex[10]+data_hex[11],16) 
        except: 
            pm25_cf=0
        try: 
            pm10_cf=int(data_hex[12]+data_hex[13]+data_hex[14]+data_hex[15],16) 
        except: 
            pm10_cf=0
        try: 
            pm1=int(data_hex[16]+data_hex[17]+data_hex[18]+data_hex[19],16) 
        except: 
            pm1=0
        try: 
            pm25=int(data_hex[20]+data_hex[21]+data_hex[22]+data_hex[23],16) 
        except: 
            pm25=0
        try: 
            pm10=int(data_hex[24]+data_hex[25]+data_hex[26]+data_hex[27],16) 
        except: 
            pm10=0
        try:
            pmT=int(round(int(data_hex[44]+data_hex[45]+data_hex[46]+data_hex[47],16)/10,0))
        except:
            pmT = 0
        try:
            pmH=int(round(int(data_hex[48]+data_hex[49]+data_hex[50]+data_hex[51],16)/10,0))
        except:
            pmH = 0


        if self.debug: print ("pm1_cf: {}".format(pm1_cf))
        if self.debug: print ("pm25_cf: {}".format(pm25_cf))
        if self.debug: print ("pm10_cf: {}".format(pm10_cf))
        if self.debug: print ("pm1: {}".format(pm1))
        if self.debug: print ("pm25: {}".format(pm25))
        if self.debug: print ("pm10: {}".format(pm10))
        if self.debug: print ("pmT: {}".format(pmT))
        if self.debug: print ("pmH: {}".format(pmH))
        data = [pm1_cf, pm10_cf, pm25_cf, pm1, pm10, pm25, pmT, pmH]
        self.serial.close()
        return data

    def read(self, argv):
        tty=argv[0:]
        self.conn_serial_port(tty)
        if self.check_keyword() == True:
            self.data = self.read_data()
            if self.debug: print (self.data)
            return self.data
        else:
            return 0

