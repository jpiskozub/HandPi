import board
import busio
i2c = busio.I2C(board.SCL, board.SDA)

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.ads1x15 import Mode
from adafruit_ads1x15.analog_in import AnalogIn

import numpy as np

version = "0.0.1"

ads0 = ADS.ADS1115(i2c, address=0x48, data_rate=860, gain=2/3)  # U4
ads1 = ADS.ADS1115(i2c, address=0x49, data_rate=860, gain=2/3)  # U3
ads2 = ADS.ADS1115(i2c, address=0x4a, data_rate=860, gain=2/3)  # U1
ads3 = ADS.ADS1115(i2c, address=0x4b, data_rate=860, gain=2/3)  # U2

#ads0.mode = Mode.CONTINUOUS

P1_1 = AnalogIn(ads1, ADS.P3) # P1_1 PIN:12
P1_2 = AnalogIn(ads1, ADS.P0) # P1_2 PIN:10
P2_1 = AnalogIn(ads3, ADS.P3) # P2_1 PIN:6
P2_2 = AnalogIn(ads3, ADS.P0) # P2_2 PIN:8
P3_1 = AnalogIn(ads2, ADS.P3) # P3_1 PIN:2
P3_2 = AnalogIn(ads2, ADS.P0) # P3_2 PIN:4
P4_1 = AnalogIn(ads2, ADS.P1) # P4_1 PIN:1
P4_2 = AnalogIn(ads2, ADS.P2) # P4_2 PIN:3
P5_1 = AnalogIn(ads3, ADS.P1) # P5_1 PIN:5
P5_2 = AnalogIn(ads3, ADS.P2) # P5_2 PIN:7

Spare0 = AnalogIn(ads0, ADS.P0)
Spare1 = AnalogIn(ads0, ADS.P1)
Spare2 = AnalogIn(ads0, ADS.P2)
Spare3 = AnalogIn(ads0, ADS.P3)
Spare5 = AnalogIn(ads1, ADS.P1)
Spare6 = AnalogIn(ads1, ADS.P2)

def readADC():
    ADC_vect = []
    ADC_vect.append(P1_1.value)
    ADC_vect.append(P1_2.value)
    ADC_vect.append(P2_1.value)
    ADC_vect.append(P2_2.value)
    ADC_vect.append(P3_1.value)
    ADC_vect.append(P3_2.value)
    ADC_vect.append(P4_1.value) 
    ADC_vect.append(P4_2.value) 
    ADC_vect.append(P5_1.value) 
    ADC_vect.append(P5_2.value) 
    return ADC_vect

while True:
    print ("HandPi ver:", version)
    mode = input("Select operation mode: \n D - Debug Mode \t E - Examination Mode")

    if mode == 'D' or 'd':
        try:
            while True:
                readADC()
                print (readADC())
                
        except KeyboardInterrupt:
            print('Interrupted!')

    if mode == 'E'  or 'e':
        try:
            sign_type = input("Select examined sign type: /n S - Static Signs /t D - Dynamic Signs")
            if sign_type == 'S' or 's':
                    while True:
                        sign = input("Select sign to be performed: /t")
                        for i in range(10):
                            readADC()
                            print (readADC())
        except KeyboardInterrupt:
            print('Interrupted!')