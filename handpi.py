import board
import busio
i2c = busio.I2C(board.SCL, board.SDA)

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.ads1x15 import Mode
from adafruit_ads1x15.analog_in import AnalogIn
from time import sleep

import numpy as np

version = "UDP"

UDP_IP = "192.168.43.140"
UDP_PORT = 65000


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)




ads1 = ADS.ADS1115(i2c, address=0x4a, data_rate=860, gain=2/3)  # U1
ads2 = ADS.ADS1115(i2c, address=0x4b, data_rate=860, gain=2/3)  # U2
ads3 = ADS.ADS1115(i2c, address=0x49, data_rate=860, gain=2/3)  # U3
ads4= ADS.ADS1115(i2c, address=0x48, data_rate=860, gain=2/3)  # U4


P1_1 = AnalogIn(ads3, ADS.P3) # P1_1 PIN:12
P1_2 = AnalogIn(ads3, ADS.P1) # P1_2 PIN:9
P2_1 = AnalogIn(ads2, ADS.P0) # P2_1 PIN:6
P2_2 = AnalogIn(ads2, ADS.P3) # P2_2 PIN:8
P3_1 = AnalogIn(ads1, ADS.P0) # P3_1 PIN:2
P3_2 = AnalogIn(ads1, ADS.P3) # P3_2 PIN:4
P4_1 = AnalogIn(ads1, ADS.P1) # P4_1 PIN:1
P4_2 = AnalogIn(ads1, ADS.P2) # P4_2 PIN:3
P5_1 = AnalogIn(ads2, ADS.P2) # P5_1 PIN:7
P5_2 = AnalogIn(ads2, ADS.P1) # P5_2 PIN:7

Spare0 = AnalogIn(ads3, ADS.P0)
Spare1 = AnalogIn(ads3, ADS.P2)
Spare2 = AnalogIn(ads4, ADS.P1)
Spare3 = AnalogIn(ads4, ADS.P0)
Spare5 = AnalogIn(ads4, ADS.P2)
Spare6 = AnalogIn(ads4, ADS.P3)

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

def readADC_voltage():
    ADC_voltage_vect = []
    ADC_voltage_vect.append(P1_1.voltage)
    ADC_voltage_vect.append(P1_2.voltage)
    ADC_voltage_vect.append(P2_1.voltage)
    ADC_voltage_vect.append(P2_2.voltage)
    ADC_voltage_vect.append(P3_1.voltage)
    ADC_voltage_vect.append(P3_2.voltage)
    ADC_voltage_vect.append(P4_1.voltage) 
    ADC_voltage_vect.append(P4_2.voltage) 
    ADC_voltage_vect.append(P5_1.voltage) 
    ADC_voltage_vect.append(P5_2.voltage) 
    return ADC_voltage_vect

def self_diag(shortcircuit_threshold):
    ADC_diag_buff=[]
    for i in range (10):
        ADC_diag_buff.append(readADC())
    diag_avr=np.array(ADC_diag_buff)
    diag_mean = [diag_avr.mean(axis=0),
                 diag_avr.mean(axis=1), 
                 diag_avr.mean(axis=2), 
                 diag_avr.mean(axis=3), 
                 diag_avr.mean(axis=4), 
                 diag_avr.mean(axis=5), 
                 diag_avr.mean(axis=6), 
                 diag_avr.mean(axis=7), 
                 diag_avr.mean(axis=8), 
                 diag_avr.mean(axis=9), 
                 diag_avr.mean(axis=10)]
    for i in diag_mean:
        if diag_mean[i]>=shortcircuit_threshold:
            print("Shortcircuit on channel:", i)

while True:
    print ("HandPi ver:", version)
    mode = input("Select operation mode: \n D - Debug Mode \t E - Examination Mode")

    if mode == 'D' or 'd':
        self_diag(24000)
        try:
            while True:
                readADC()
                sock.sendto(readADC().encode('utf-8'), ("192.168.43.140", 5005))
                sleep(1)
                
        except KeyboardInterrupt:
            print('Interrupted!')

 
       