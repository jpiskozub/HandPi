
#!/usr/bin/env python3


import board
import busio
import paho.mqtt.client as mqtt

mqttc=mqtt.Client(client_id='handpi')

broker= '192.168.0.100'
port=1883
topic='handpi'



i2c = busio.I2C(board.SCL, board.SDA)

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.ads1x15 import Mode
from adafruit_ads1x15.analog_in import AnalogIn


import adafruit_bno055

from alive_progress import alive_bar

import psycopg as psql


import pandas as pd
import numpy as np

import time #Temporary for diagnostics
from queue import Queue



ads1 = ADS.ADS1115(i2c, address=0x4a, data_rate=860, gain=2/3)  # U1
ads2 = ADS.ADS1115(i2c, address=0x4b, data_rate=860, gain=2/3)  # U2
ads3 = ADS.ADS1115(i2c, address=0x49, data_rate=860, gain=2/3)  # U3
ads4= ADS.ADS1115(i2c, address=0x48, data_rate=860, gain=2/3)  # U41


sensor = adafruit_bno055.BNO055_I2C(i2c) #IMU

#BNO_AXIS_REMAP = { 'x': BNO055.AXIS_REMAP_X,
#                  'y': BNO055.AXIS_REMAP_Z,
#                  'z': BNO055.AXIS_REMAP_Y,
#                  'x_sign': BNO055.AXIS_REMAP_POSITIVE,
#                  'y_sign': BNO055.AXIS_REMAP_POSITIVE,
#                  'z_sign': BNO055.AXIS_REMAP_NEGATIVE }
#remap=(0x00,0x02,0x01,0x00,0x00,0x01)
remap=(0,1,2,1,1,0) # Position P2 as in datasheet p.25
sensor.axis_remap = remap

print("Axis mapped as:{}".format(sensor.axis_remap))

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
    print('Shortcircuits on ADC_: ', result[0], sep='\t')
    sc_channels=result[0]
    for x in sc_channels:
        print(ADC_channels[x])
    return sc_channels
    
def exam_data():

    gender = input ("State a gender of a subject \t [M/F]")
    mscd = input ("Does subjcet has any muscosceletal disorders? \t [Y/N]")
    age = input ("State an age of a subject:")
    palm = input ("State a palm size of a subject (use '.' as a decimal delimiter):")
    
    return gender, age, palm, mscd


def repeat_prompt(countdown):
    print('Repeating:')
    for i in range(1,countdown+1):
        print('{0}'.format(i))
        time.sleep(1)
        
        
def get_exam_id(db_connector, db_cursor):
    db_cursor.execute("SELECT MAX(exam_id) FROM examination;") #May be done with RETURN SQL statement - To be explored
    last_exam_id=db_cursor.fetchone()
    return last_exam_id[0]

def get_gesture_id(db_connector, db_cursor):
    db_cursor.execute("SELECT MAX(gesture_id) FROM static_gestures;") #May be done with RETURN SQL statement - To be explored
    last_static_id=list(db_cursor.fetchone())
    db_cursor.execute("SELECT MAX(gesture_id) FROM dynamic_gestures;") #May be done with RETURN SQL statement - To be explored
    last_dynamic_id=list(db_cursor.fetchone())
    
    if last_static_id[0] == None:
        last_static_id[0]=0
    if last_dynamic_id[0] == None:
        last_dynamic_id[0]=0
        
    if last_static_id[0] == 0 and last_dynamic_id[0] == 0:
        return 0
    elif int(last_static_id[0]) > int(last_dynamic_id[0]):
        return int(last_static_id[0])
    else:
        return int(last_dynamic_id[0])
        
        
def sql_insert(db_connector, db_cursor, queue, sign, sample_size):
    sign_type = sign_types_dict[sign]
    
    last_exam_id = get_exam_id(db_connector, db_cursor)
    last_gesture_id = get_gesture_id(db_connector, db_cursor)
    
    for i in range(sample_size):
        if  sign_type == 'static':
            try:
                SQL_static_insert = 'INSERT INTO static_gestures (exam_id, p1_1, p1_2, p2_1, p2_2, p3_1, p3_2, p4_1, p4_2, p5_1, p5_2, gyro_x, gyro_y, gyro_z, acc_x, acc_y, acc_z, gesture, tmstmp, gesture_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                db_cursor.execute(SQL_static_insert,(last_exam_id, *queue.get(),last_gesture_id+1))      
                db_connector.commit() 
            except psql.errors.UndefinedColumn :
                db_cursor.rollback()
                if 'None' in position_readings_temp:
                    position_readings_temp = (0,0,0)
                else:
                    movement_readings_temp = (0,0,0)
                db_cursor.execute(" INSERT INTO static_gestures (exam_id, p1_1, p1_2, p2_1, p2_2, p3_1, p3_2, p4_1, p4_2, p5_1, p5_2, gyro_x, gyro_y, gyro_z, acc_x, acc_y, acc_z, gesture, tmstmp) VALUES ({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, {16}, '{17}', '{18}'); ".format(last_id[0],  *ADC_readings_temp, *position_readings_temp,  *movement_readings_temp, sign, pd.Timestamp.now() ))        
            db_connector.commit()
        else:
            try:
                SQL_dynamic_insert = 'INSERT INTO dynamic_gestures (exam_id, p1_1, p1_2, p2_1, p2_2, p3_1, p3_2, p4_1, p4_2, p5_1, p5_2, gyro_x, gyro_y, gyro_z, acc_x, acc_y, acc_z, gesture, tmstmp, gesture_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                db_cursor.execute(SQL_dynamic_insert,(last_exam_id, *queue.get(),last_gesture_id+1))      
                db_connector.commit() 
            except psql.errors.UndefinedColumn :
                db_cursor.rollback()
                if 'None' in position_readings_temp:
                    position_readings_temp = (0,0,0)
                else:
                    movement_readings_temp = (0,0,0)
                db_cursor.execute(" INSERT INTO dynamic_gestures (exam_id, p1_1, p1_2, p2_1, p2_2, p3_1, p3_2, p4_1, p4_2, p5_1, p5_2, gyro_x, gyro_y, gyro_z, acc_x, acc_y, acc_z, gesture, tmstmp) VALUES ({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, {16}, '{17}', '{18}'); ".format(last_id[0],  *ADC_readings_temp, *position_readings_temp,  *movement_readings_temp, sign, pd.Timestamp.now() ))        
            db_connector.commit()
            
            
            
def main():
    while True:
    #print ("HandPi ver:", version)
    
        
        SAMPLE_SIZE = 75
        SHORT_CIRCUT_THRESHOLD = 22000
        
        
        self_diag(SHORT_CIRCUT_THRESHOLD)
        mqttc.connect(broker,port)
    
        psqlconn = psql.connect(dbname = 'handpi', user = 'handpi', password = 'raspberryhandpi', host = broker)
        psqlcur = psqlconn.cursor()
    
        
        mode = input("Select operation mode: \n 1 - Debug Mode \t 2 - Examination Mode")
        
        
    
        if mode == '1':
            try:
                while True:
                    msg = (*readADC(), *sensor.euler, *sensor.linear_acceleration, *sensor.gyro, *sensor.magnetic, *sensor.acceleration )
                    print (msg)
                    mqttc.publish(topic,str(msg))
            except KeyboardInterrupt:
                print('Interrupted!')
    
        else:

            try:
            
                
                initals = input ('Please provide subject initials:')
                psqlcur.execute("INSERT INTO examination (patient_initials) VALUES ('{0}');".format(initals))
    
                psqlcur.execute("SELECT MAX(exam_id) FROM examination;") #May be done with RETURN SQL statement - To be explored
    
                last_id=psqlcur.fetchone()
                (gender, age, palm, mscd) = exam_data()
                psqlcur.execute("INSERT INTO patient_data (exam_id, gender, age, mcsd, palm_size) VALUES ({0}, '{1}', {2}, '{3}', {4});".format(max(last_id), gender, age, mscd, palm ))
                psqlqueue = Queue()

                while True:
                    sign = input("Select sign to be performed: \t")
                    reps = int(input("Enter the number of repetitions: \t"))
                    if sign not in sign_types_dict:
                        raise Exception ('{0} is not a valid gesture'.format(sign))
                           
                    
                    ADC_readings_temp=[]
                    position_readings_temp=[]
                    movement_readings_temp=[]
                        
                    print('Commencing procedure')
                    for r in range(int(reps)):
                       time.sleep(1)
                    
    
                       t=time.process_time()
                       with alive_bar(SAMPLE_SIZE, ctrl_c=False, bar='filling',title='Gesture {}'.format(sign)) as bar:
                           for i in range(SAMPLE_SIZE):
                               ADC_readings_temp = readADC()
                               position_readings_temp = sensor.euler
                               movement_readings_temp = sensor.linear_acceleration
                               psqlqueue.put((*ADC_readings_temp, *position_readings_temp,  *movement_readings_temp, sign, pd.Timestamp.now()))
                               bar()
                       elapsed_time = time.process_time()-t
                       print (elapsed_time)
                       self_diag(SHORT_CIRCUT_THRESHOLD)
                       sql_insert(psqlconn, psqlcur, psqlqueue, sign, SAMPLE_SIZE)
                       if r<reps-1:
                            repeat_prompt(3)
                        
                       
    
            except KeyboardInterrupt:
                psqlconn.commit()
                psqlcur.close()
                psqlconn.close()
                print('Examination stopped')

if __name__ == '__main__':
    
    main()
       
