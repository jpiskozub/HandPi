import board
import busio

i2c = busio.I2C(board.SCL, board.SDA)

import adafruit_ads1x15.ads1115 as ADS
import adafruit_bno055

import numpy as np
from adafruit_ads1x15.ads1x15 import Mode
from adafruit_ads1x15.analog_in import AnalogIn

import csv
import time
from tqdm import trange





version = "main"


ads1 = ADS.ADS1115(i2c, address=0x4a, data_rate=860, gain=2/3)  # U1
ads2 = ADS.ADS1115(i2c, address=0x4b, data_rate=860, gain=2/3)  # U2
ads3 = ADS.ADS1115(i2c, address=0x49, data_rate=860, gain=2/3)  # U3
ads4= ADS.ADS1115(i2c, address=0x48, data_rate=860, gain=2/3)  # U4

remap_P6= (0x00,0x01,0x02,0x00,0x01,0x01)

sensor = adafruit_bno055.BNO055_I2C(i2c) #IMU
#sensor.axis_remap()


P1_1 = AnalogIn(ads3, ADS.P3) # P1_1 PIN:12
P1_2 = AnalogIn(ads3, ADS.P1) # P1_2 PIN:9
P2_1 = AnalogIn(ads2, ADS.P0) # P2_1 PIN:6
P2_2 = AnalogIn(ads2, ADS.P3) # P2_2 PIN:8
P3_1 = AnalogIn(ads1, ADS.P0) # P3_1 PIN:2
P3_2 = AnalogIn(ads1, ADS.P3) # P3_2 PIN:4
P4_1 = AnalogIn(ads1, ADS.P1) # P4_1 PIN:1
P4_2 = AnalogIn(ads1, ADS.P2) # P4_2 PIN:3
P5_1 = AnalogIn(ads2, ADS.P2) # P5_1 PIN:7
P5_2 = AnalogIn(ads2, ADS.P1) # P5_2 PIN:5

Spare0 = AnalogIn(ads3, ADS.P0)
Spare1 = AnalogIn(ads3, ADS.P2)
Spare2 = AnalogIn(ads4, ADS.P1)
Spare3 = AnalogIn(ads4, ADS.P0)
Spare5 = AnalogIn(ads4, ADS.P2)
Spare6 = AnalogIn(ads4, ADS.P3)

ADC_channels=['P1_1', 'P1_2', 'P2_1', 'P2_2', 'P3_1', 'P3_2', 'P4_1', 'P4_2', 'P5_1', 'P5_2']
IMU_channels = ['Euler_x', 'Euler_y', 'Euler_z', 'Acc_x', 'Acc_y', 'Acc_z']
fmt = "%5.5s","%5.5s","%5.5s","%5.5s","%5.5s","%5.5s","%5.5s","%5.5s","%5.5s","%5.5s","%5.7s","%5.7s","%5.7s","%5.7s","%5.7s","%5.7s","%s","%s"

sign_types = ['static', 'dynamic']
sign_types_dict = {'a': sign_types[0],
                   'ą': sign_types[1],
                   'b': sign_types[0],
                   'c': sign_types[0],
                   'ć': sign_types[1],
                   'ch': sign_types[1],
                   'cz': sign_types[1],
                   'd': sign_types[1],
                   'e': sign_types[0],
                   'ę': sign_types[1],
                   'f': sign_types[1],
                   'g': sign_types[1],
                   'h': sign_types[1],
                   'i': sign_types[0],
                   'j': sign_types[1],
                   'k': sign_types[1],
                   'l': sign_types[0],
                   'ł': sign_types[1],
                   'm': sign_types[0],
                   'n': sign_types[0],
                   'ń': sign_types[1],
                   'o': sign_types[0],
                   'ó': sign_types[1],
                   'p': sign_types[0],
                   'r': sign_types[0],
                   'rz': sign_types[1],
                   's': sign_types[0],
                   'ś': sign_types[1],
                   'sz': sign_types[1],
                   't': sign_types[0],
                   'u': sign_types[0],
                   'w': sign_types[0],
                   'y': sign_types[0],
                   'z': sign_types[1],
                   'ź': sign_types[1],
                   'ż': sign_types[1]}


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
        diag_vect=np.array(ADC_diag_buff)

    result = np.where(diag_vect.mean(axis=0) >= shortcircuit_threshold)
    print('Shortcircuits on ADC_: ', result[0], sep='\n')
    sc_channels=result[0]
    for x in sc_channels:
        print(ADC_channels[x])
    return sc_channels
    




while True:
    print ("HandPi ver:", version)
    
    self_diag(21000)
    loop_time = 100
    
    
    
    mode = input("Select operation mode: \n 1 - Debug Mode \t 2 - Examination Mode")
    
    

    if mode == 1:
        try:
            while True:
                print (readADC(),sensor.acceleration, sensor.magnetic, sensor.gyro,sensor.euler,sensor.linear_acceleration)
        except KeyboardInterrupt:
            print('Interrupted!')

    else:
        with open("/home/pi/"+time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())+".csv", mode='w') as file:
            writer = csv.writer(file,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
            writer.writerow([ADC_channels, IMU_channels])
            
            try:
                while True:
                    sign = input("Select sign to be performed: \t")
                    ADC_readings_temp=[]
                    position_readings_temp=[]
                    movement_readings_temp=[]
                    try:
                        if sign in sign_types_dict:
                            sign_type = sign_types_dict[sign]
                    except:
                        print('{0} is not in dictionary.'.format(sign))
                    for i in trange(loop_time):
                        ADC_readings_temp.append(readADC())
                        position_readings_temp.append(sensor.euler)
                        movement_readings_temp.append(sensor.linear_acceleration)
                    signarr = np.array([sign for i in range(loop_time)],dtype='str')
                    typearr = np.array([sign_type for i in range(loop_time)],dtype='str')
                    result = np.concatenate((ADC_readings_temp, position_readings_temp, movement_readings_temp),axis=1)
                    result = np.append(result,np.column_stack((signarr, typearr)),axis = 1)
                    print(result)
                    self_diag(21000)
                    np.savetxt(file, result, delimiter=',', fmt= fmt)
            except KeyboardInterrupt:
                print('Interrupted!')

 
       