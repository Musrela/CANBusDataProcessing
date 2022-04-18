#File to read the JSON file and process the CAN bus data in the following ways:
# 1. Read the file and retrieve the list of dictionaries.
# 2. Print the first 10 signal enteries of the file.  
# 3. Print all the different types of signals. Ask the user to select 1 and print the number of occurances and value range.
# 4. Calculate the vehicle trip time and trip distance.
# 5. Plot each signal type versus timestamp.
# 6. Compute the max and average vehicle speeds.
# 7. Trace the vehicle path on Google Map.
# 8. Calculate the mileage of the car using the given data in the file.

import os
import json
import pprint
import matplotlib.pyplot as pl
from pylab import *
import numpy as np
import pygmaps
import re
import time
import webbrowser



#store the path of the JSON file

#json_file=json_file.decode("utf-8-sig").encode("utf-8")
# Creates a list of the dictionaries present in the JSON and returns this list.
#@input - the file path
#@return - list of dictionaries
log_file = os.path.abspath("/home/enb/v2x/V2Xdataprocessing/v2x_tx.log")
json_file = os.path.abspath("/home/enb/v2x/V2Xdataprocessing/v2x_tx.json")
js_file = os.path.abspath("/home/enb/v2x/V2Xdataprocessing/map/gpsdata.js")
html_file = os.path.abspath("/home/enb/v2x/V2Xdataprocessing/map/index.html")
msgCount = []
vehicle_id = []
DSecond = []
latitude = []
longitude = []
elevation = []#海拔
transmission = []#档位
speed = []
heading = []
long_Acceleration = []
lat_Acceleration = []
vert_Acceletation = []
yawrate = []
brakePadel =[]
wheelBrakes =[]
traction = []
Abs =[]
scs =[]
brakeboost =[]
auxbrakes =[]
width =[]
length =[]
height =[]
classification = []

def func0(log_file):


    Handle = open (log_file,'r')
    num = -1
    lineNum = 0
    fileList = []
    if os.path.exists(json_file):  # 如果文件存在
    # 删除文件，可使用以下两种方法。
        os.remove(json_file)  
    #os.unlink(path)
    else:
        print('no such file:%s'%json_file)  # 则返回文件不存在
    if os.path.exists(js_file):  # 如果文件存在
        # 删除文件，可使用以下两种方法。
        os.remove(js_file)  
        #os.unlink(path)
    else:
       print('no such file:%s'%js_file)  # 则返回文件不存在

    for line in Handle:
        fileList.append(line)
    for new_line in fileList:
        lineNum +=1
        if re.search('BasicSafetyMessage',new_line):
            num +=1
            struct_time = time.strptime(fileList[lineNum-2].strip(), "%a %b %d %H:%M:%S %Y")# Thu Mar 17 17:03:35 2022
            timestamp= time.mktime(struct_time)
            #print("时间戳 %d " %timestamp)
            name_msgCount,value_msgCount = fileList[lineNum].strip().split(':',1)
            msgCount.append(int(value_msgCount))
            name_vehicle_id,value_vehicle_id = fileList[lineNum+1].strip().split(':',1)
            vehicle_id.append(value_vehicle_id)
 #time.asctime(fileList[lineNum+1]）
        if re.search('secMark',new_line):
            name_DSecond,value_DSecond = fileList[lineNum-1].strip().split(':',1)
            DSecond.append(int(value_DSecond))
            #print(fileList[lineNum+2])
            name_latitude,value_latitude = fileList[lineNum+1].strip().split(':',1)
            latitude.append(int(value_latitude))
            name_longitude,value_longitude = fileList[lineNum+2].strip().split(':',1)
            longitude.append(int(value_longitude))
            name_elevation,value_elevation = fileList[lineNum+3].strip().split(':',1)
            elevation.append(int(value_elevation))
            name_transmission,value_transmission = fileList[lineNum+5].strip().split(':',1)
            transmission.append(int(value_transmission.strip().split(' ',1)[0]))
            name_speed,value_speed = fileList[lineNum+6].strip().split(':',1)
            speed.append(int(value_speed))
            name_heading,value_heading = fileList[lineNum+7].strip().split(':',1)
            heading.append(int(value_heading))
            while(int(latitude[num]) >= 100) :
                latitude[num]=latitude[num]/10;
            while(longitude[num] >= 1000) :
                longitude[num]=longitude[num]/10;

        if re.search('AccelerationSet4Way',new_line):
            name_long_Acceleration,value_long_Acceleration = fileList[lineNum].strip().split(':',1)
            long_Acceleration.append(int(value_long_Acceleration))
            #print(fileList[lineNum+2])
            name_lat_Acceleration,value_lat_Acceleration = fileList[lineNum+1].strip().split(':',1)
            lat_Acceleration.append(int(value_lat_Acceleration))
            name_vert_Acceletation,value_vert_Acceletation = fileList[lineNum+2].strip().split(':',1)
            vert_Acceletation.append(int(value_vert_Acceletation))           
            name_yawrate,value_yawrate = fileList[lineNum+3].strip().split(':',1)
            yawrate.append(int(value_yawrate))
        if re.search('BrakeSystemStatus',new_line):
            name_brakePadel,value_brakePadel = fileList[lineNum].strip().split(':',1)
            brakePadel.append(int(value_brakePadel.strip().split(' ',1)[0]))
            name_traction,value_traction = fileList[lineNum+1].strip().split(':',1)
            traction.append(int(value_traction.strip().split(' ',1)[0]))
            name_Abs,value_Abs = fileList[lineNum+2].strip().split(':',1)
            Abs.append(int(value_Abs.strip().split(' ',1)[0]))
            name_scs,value_scs = fileList[lineNum+3].strip().split(':',1)
            scs.append(int(value_scs.strip().split(' ',1)[0]))
        if re.search('VehicleSize',new_line):
            name_width,value_width = fileList[lineNum].strip().split(':',1)
            width.append(int(value_width))
            name_length,value_length = fileList[lineNum+1].strip().split(':',1)
            length.append(int(value_length))
      
        if re.search('VehicleClassification',new_line):
            name_classification,value_classification = fileList[lineNum].strip().split(':',1)
            classification.append(int(value_classification))

            #异常数据检查
            if msgCount[num]>127 or msgCount[num]<0 or (1<num and msgCount[num]!=(msgCount[num-1]+1)%128)  :
                print("\033[1;31;40m msgCount is error\033[0m","msgCount is %d  lineNum : %d" % (msgCount[num] ,lineNum-27))    
            if num >1 and vehicle_id[num]!=vehicle_id[num-1] :
                print("\033[1;31;40m vehicle_id is error\033[0m","vehicle_id is %s   lineNum : %d" % (vehicle_id[num],lineNum-26))  
            if DSecond[num]>59999 or DSecond[num]<0 or (1<num and DSecond[num]!=(DSecond[num-1]+100)%60000)   :    #毫秒数数据检查
                print("\033[1;31;40m DSecond is error\033[0m","DSecond is %d  lineNum : %d" % (DSecond[num],lineNum-25))                           
            if latitude[num]>53.33 or latitude[num]<3.52 :
                print("\033[1;3 #1;40m latitude is error\033[0m","latitude is %f  lineNum : %d" % (latitude[num],lineNum-23))
            if longitude[num]>135.2 or longitude[num]<73.40 :
                print("\033[1;31;40m longitude is error\033[0m","longitude is %f lineNum : %d" %( longitude[num],lineNum-22))      
            if elevation[num]>3658 or elevation[num]<0 :
                print("\033[1;31;40m elevation is error\033[0m","elevation is %f lineNum : %d" % (elevation[num],lineNum-21))  
            if transmission[num]>7 or transmission[num]<0  or(transmission[num]==1 and speed[num] >0 ) : #档位数据检查
                print("\033[1;31;40m transmission is error\033[0m","transmission is %d lineNum : %d" % (transmission[num],lineNum-19))  
            if speed[num]>8191 or speed[num]<0 :
                print("\033[1;31;40m speed is error\033[0m","speed is %d lineNum : %d" % (speed[num],lineNum-18))  
            if heading[num]>28800 or heading[num]<0 :
                print("\033[1;31;40m heading is error\033[0m","heading is %d lineNum : %d" % (heading[num],lineNum-17))  
            if long_Acceleration[num]>127 or long_Acceleration[num]<-127 :
                print("\033[1;31;40m long_Acceleration is error\033[0m","long_Acceleration is %d lineNum : %d" % (long_Acceleration[num],lineNum-15))  
            if lat_Acceleration[num]>127 or lat_Acceleration[num]<-127 :
                print("\033[1;31;40m lat_Acceleration is error\033[0m","lat_Acceleration is %d lineNum : %d" %( lat_Acceleration[num],lineNum-14))  
            if vert_Acceletation[num]>127 or vert_Acceletation[num]<-127 :
                print("\033[1;31;40m vert_Acceletation is error\033[0m","vert_Acceletation is %d lineNum : %d" % (vert_Acceletation[num],lineNum-13))  
            if yawrate[num] > 32767 or yawrate[num]< -32767 :
                print("\033[1;31;40m yawrate is error\033[0m","yawrate is %d lineNum : %d" % (yawrate[num],lineNum-12))  
            if brakePadel[num] > 2 or brakePadel[num]< 0 :
                print("\033[1;31;40m brakePadel is error\033[0m","brakePadel is %d lineNum : %d" % (brakePadel[num],lineNum-9))  
            if traction[num] > 3 or traction[num]< 0 :
                print("\033[1;31;40m traction is error\033[0m","traction is %d lineNum : %d" % (traction[num],lineNum-8))  
            if Abs[num] > 3 or Abs[num]< 0 :
                print("\033[1;31;40m Abs is error\033[0m","Abs is %d lineNum : %d" % (Abs[num],lineNum-7))  
            if scs[num] > 3 or scs[num]< 0 :
                print("\033[1;31;40m scs is error\033[0m","scs is %d lineNum : %d" %( scs[num],lineNum-6))  
            if width[num] > 1023 or width[num]< 0 :
                print("\033[1;31;40m width is error\033[0m","width is %d lineNum : %d" % (width[num],lineNum-3))  
            if length[num] > 4095 or length[num]< 0 :
                print("\033[1;31;40m length is error\033[0m","length is %d lineNum : %d" % (length[num],lineNum-2))                 
            if classification[num] > 7 or classification[num]< 0 :#车辆分类数据检查
                print("\033[1;31;40m classification is error\033[0m","classification is %d lineNum : %d" % (classification[num],lineNum+1)) 


            with open('v2x_tx.json','a+',newline='\n') as f:
                f.writelines('{"name":"msgCount","value":'+str(msgCount[num])+',"timestamp":'+str(round(timestamp,5))+'}'+'\n')
                json.dump({"name":"vehicle_id","value":vehicle_id[num],"timestamp":round(timestamp,5)},f)
                f.write('\n')
                json.dump({"name":"DSecond","value":int(DSecond[num]),"timestamp":round(timestamp,5)},f)
                f.write('\n')
                json.dump({"name":"latitude","value":round(latitude[num],5),"timestamp":round(timestamp,5)},f)
                f.write('\n')
                json.dump({"name":"longitude","value":round(longitude[num],5),"timestamp":round(timestamp,5)},f)
                f.write('\n')
                json.dump({"name":"elevation","value":round(elevation[num]),"timestamp":round(timestamp,5)},f)
                f.write('\n')
                json.dump({"name":"transmission","value":int(transmission[num]),"timestamp":round(timestamp,5)},f) 
                f.write('\n')   
                json.dump({"name":"speed","value":int(speed[num]),"timestamp":round(timestamp,5)},f) 
                f.write('\n') 
                json.dump({"name":"heading","value":int(heading[num]),"timestamp":round(timestamp,5)},f) 
                f.write('\n') 
                json.dump({"name":"long_Acceleration","value":int(long_Acceleration[num]),"timestamp":round(timestamp,5)},f) 
                f.write('\n') 
                json.dump({"name":"lat_Acceleration","value":int(lat_Acceleration[num]),"timestamp":round(timestamp,5)},f) 
                f.write('\n') 
                json.dump({"name":"vert_Acceletation","value":int(vert_Acceletation[num]),"timestamp":round(timestamp,5)},f) 
                f.write('\n') 
                json.dump({"name":"yawrate","value":int(yawrate[num]),"timestamp":round(timestamp,5)},f) 
                f.write('\n') 
                json.dump({"name":"brakePadel","value":int(brakePadel[num]),"timestamp":round(timestamp,5)},f) 
                f.write('\n') 
                json.dump({"name":"traction","value":int(traction[num]),"timestamp":round(timestamp,5)},f) 
                f.write('\n')     
                json.dump({"name":"Abs","value":int(Abs[num]),"timestamp":round(timestamp,5)},f) 
                f.write('\n')      
                json.dump({"name":"scs","value":int(scs[num]),"timestamp":round(timestamp,5)},f) 
                f.write('\n')        
                json.dump({"name":"width","value":int(width[num]),"timestamp":round(timestamp,5)},f) 
                f.write('\n')   
                json.dump({"name":"length","value":int(length[num]),"timestamp":round(timestamp,5)},f) 
                f.write('\n')      
                json.dump({"name":"classification","value":int(classification[num]),"timestamp":round(timestamp,5)},f) 
                f.write('\n') 
    with open(js_file,'a+',newline='\n') as f:
        f.write('var gpsdata = [\n')
        for i in range(num):
            f.writelines('{lng:'+str(round(longitude[i],5))+',lat:'+str(round(latitude[i],5))+'},\n')
        f.write(']\n')


def func1(json_file):
    list_of_dicts = [] #create an empty list
    with open(json_file) as fp:
        for each_dict in fp: #for each dictionay in the file
            list_of_dicts.append(json.loads(each_dict)) #append each dictionary to the list
    return list_of_dicts


# Pretty prints the the first 10 signal enteries
#@input - list of the dictionaries 
def func2(list_from_file):
    print("The first 10 signal entries:")
    pprint.pprint(list_from_file[:10],indent = 4, width = 105) #print the first 10 signal enteries with indent as 4 and the width of each line as 105
    print ("\n")


# Parses the list of dictionaries and prints the different signal names.
# It then asks the user to select 1 of these signals and prints the number 
# of occurances and value range of this signal.
#@input - list of the dictionaries
def func3(list_from_file):
    print("The different signal names are:")
    set_of_values = set()   #create an empty set. Use a set to avoid storing repeated values.
    for each_dict in list_from_file:
        if 'name' in each_dict: 
            set_of_values.add(each_dict['name']) # store the values of each key 'name' in a list
    for signals in set_of_values:
        print(signals)

    print ("\nEnter a signal name from the above list of signals:")
    signal_name = input() #Take input from the user for the dersired signal
    list_of_values = signal_values(list_from_file, signal_name) #Create a list of all the odometer values 
    print ("Number of occurances of the signal \"" + signal_name + "\": " + str(len(list_of_values)))
    print ("Range of values of the signal \"" + signal_name + "\": " + str(min(list_of_values)) + " to " + str(max(list_of_values))) # Print the range of the signal value by computing the min amd max value present in the list.


# Parses the list of dictionaries and retrieves the first and last timestamp and odometer values.
# Using these values, it calculates the trip time period and trip distance.
# @input - list of the dictionaries
# @return - trip distance and time period
def func4(list_from_file):
    list_of_odometer_values = signal_values(list_from_file, "odometer") #Create a list of all the odometer values 
    list_of_timestamp = []
    for each_dict in list_from_file:
        if each_dict.get('timestamp'):
            list_of_timestamp.append(each_dict.get('timestamp')) #Create a list of all timestamp values
    time_period = "{:.6f}".format(list_of_timestamp[len(list_of_timestamp)-1] - list_of_timestamp[0]) #Calculate the time period by subtracting the last and first timestamp.
    trip_distance = "{:.6f}".format(list_of_odometer_values[len(list_of_odometer_values)-1] - list_of_odometer_values[0]) #Calculate the trip distance by subtracting the last and first odometer value.
    print ("\nThe trip time period of vehicle is: "+ time_period + " seconds")
    print ("The trip distance is: " + trip_distance + " miles")
    return time_period,trip_distance


# Plot all the signal types versus timestamp.
# This function creates 3 figures(windows) with 4 plots each.
# @input - list of the dictionaries
def func5(list_from_file):

    figure(0) #Create a new figure window (0)
    msgCount = signal_values(list_from_file, "msgCount") # Get the odometer values
    msgCount_time = timestamp_values(list_from_file, "msgCount") #Get the corresponding timestamp values
    pl.subplot(2,2,1) #Divide the figure to contain 4 subplots (2 rows, 2 colums, the postion of this subplot is 1).
    pl.xlabel("Timestamp (s)")
    pl.ylabel("msgCount (miles)")
    pl.plot(np.array(msgCount_time),np.array(msgCount)) #plot the time on x axis and odometer values on y axis

    latitude = signal_values(list_from_file, "latitude")
    latitude_time = timestamp_values(list_from_file, "latitude") 
    pl.subplot(2,2,2) #position of this subplot is 2
    pl.xlabel("Timestamp (s)")
    pl.ylabel("Latitude (degrees)")
    pl.plot(np.array(latitude_time),np.array(latitude))

    longitude = signal_values(list_from_file, "longitude")
    longitude_time = timestamp_values(list_from_file, "longitude")
    pl.subplot(2,2,3)
    pl.xlabel("Timestamp (s)")
    pl.ylabel("Longitude (degrees)")
    pl.plot(np.array(longitude_time),np.array(longitude))

    elevation = signal_values(list_from_file, "elevation")
    elevation_time = timestamp_values(list_from_file, "elevation")
    pl.subplot(2,2,4)
    pl.xlabel("Timestamp (s)")
    pl.ylabel("Elevation (degrees)")
    pl.plot(np.array(elevation_time),np.array(elevation))

    figure(1) #Create a new figure window (1)
    steering_wheel_angle = signal_values(list_from_file, "steering_wheel_angle")
    steering_wheel_angle_time = timestamp_values(list_from_file, "steering_wheel_angle")
    pl.subplot(2,2,1)
    pl.xlabel("Timestamp (s)")
    pl.ylabel("Steering Wheel Angle (degrees)")
    pl.plot(np.array(steering_wheel_angle_time),np.array(steering_wheel_angle))

    accelerator_pedal_position = signal_values(list_from_file, "accelerator_pedal_position")
    accelerator_pedal_position_time = timestamp_values(list_from_file, "accelerator_pedal_position")
    pl.subplot(2,2,2)
    pl.xlabel("Timestamp (s)")
    pl.ylabel("Accelerator Pedal Position")
    pl.plot(np.array(accelerator_pedal_position_time),np.array(accelerator_pedal_position))

    transmission_gear_position = signal_values(list_from_file, "transmission_gear_position")
    transmission_gear_position_time = timestamp_values(list_from_file, "transmission_gear_position")
    pl.subplot(2,2,3)
    pl.xlabel("Timestamp (s)")
    pl.ylabel("Transmission Gear Position")
    pl.plot(np.array(transmission_gear_position_time),np.array(transmission_gear_position))

    brake_pedal_status = signal_values(list_from_file, "brake_pedal_status")
    brake_pedal_status_time = timestamp_values(list_from_file, "brake_pedal_status")
    pl.subplot(2,2,4)
    pl.xlabel("Timestamp (s)")
    pl.ylabel("Brake Pedal Status (True/False)")
    pl.plot(np.array(brake_pedal_status_time),np.array(brake_pedal_status))

    figure(2) #Create a new figure window (2)
    speed = signal_values(list_from_file, "speed")
    vehicle_speed_time = timestamp_values(list_from_file, "speed")
    pl.subplot(2,2,1)
    pl.xlabel("Timestamp (s)")
    pl.ylabel("Vehicle Speed (miles/hour)")
    pl.plot(np.array(vehicle_speed_time),np.array(speed))

    heading = signal_values(list_from_file, "heading")
    heading_time = timestamp_values(list_from_file, "heading")
    pl.subplot(2,2,2)
    pl.xlabel("Timestamp (s)")
    pl.ylabel("Heading (gallons)")
    pl.plot(np.array(heading_time),np.array(heading))

    transmission = signal_values(list_from_file, "transmission")
    transmission_time = timestamp_values(list_from_file, "transmission")
    pl.subplot(2,2,3) #position of this subplot is 3
    pl.xlabel("Timestamp (s)")
    pl.ylabel("Transmission (Nm)")
    pl.plot(np.array(transmission_time),np.array(transmission))

    engine_speed = signal_values(list_from_file, "engine_speed")
    engine_speed_time = timestamp_values(list_from_file, "engine_speed")
    pl.subplot(2,2,4) #position of this subplot is 4
    pl.xlabel("Timestamp (s)")
    pl.ylabel("Engine Speed (rpm)")
    pl.plot(np.array(engine_speed_time),np.array(engine_speed))

    
    show() # Display all the above 3 figures.

    
# Calculates the Maximum and Average speed of the vehicle.
#@input - list of dictionaries, trip period and trip distance.
def func6(list_from_file, trip_period, trip_distance):
    list_of_vehicle_speed_values = signal_values(list_from_file, "speed") #get the list of vehicle speed values. Required to get the maximum speed.
    average_speed = "{:.6f}".format(float(trip_distance)/float(trip_period)) # Calculate the average speed = (total distance)/(total time)
    print ("\nThe maximum speed of the vehicle is: " + str(max(list_of_vehicle_speed_values)) + " miles per hour")
    print ("The averge speed of the vehicle is: " + str(average_speed) + " miles per second")


# Traces the path of the vehicle in Google Map. It uses the latitude and longitude values.
# @input - list of the dictionaries
def func7(list_from_file):
    list_of_latitude = signal_values(list_from_file, "latitude") #Get the list of latitude values 
    list_of_longitude = signal_values(list_from_file, "longitude") #Get the list of longitude values 
    #trace_map = pygmaps.maps(list_of_latitude[0], list_of_longitude[0], 16) #Initialize the pygmap variable with the first latitude and longitude values from corresponding lists
    #path = list(zip(list_of_latitude, list_of_longitude)) # Create the path using the list of latitude and longitude values
  #  trace_map.addpath(path) # Add the path in the map
    #trace_map.draw('./trace_map.html') # Create the html file to display the path on Google Map.
    #webbrowser.open('file:///home/enb/v2x/V2Xdataprocessing/map/index.html')

# Calculate the mileage of the vehicle using the trip distance and fuel consumed since restart.
# @input - list of the dictionaries, total trip distance
def func8(list_from_file, trip_distance):
    fuel_consumed_since_restart = signal_values(list_from_file, "fuel_consumed_since_restart") #Get the list of fuel_consumed_from_restart values
    fuel = fuel_consumed_since_restart[len(fuel_consumed_since_restart)-1] - fuel_consumed_since_restart[0] #Get the fuel used.
    mileage = "{:.6f}".format(float(trip_distance)/ float(fuel)) #mileage = (trip_distance)/(fuel consumed)
    print ("\nThe mileage of the car is: " + mileage + " miles/gallon")


# Get the list of values and corresponding timestamps for the required signal.
#@input - list of dictionaries, signal name
#@return - lists of values of signal and corresponding timestamp
def signal_values(list_from_file, signal_name):
    signal = [] 
    for each_dict in list_from_file: 
        if each_dict.get('name') == signal_name:
            if signal_name == "transmission_gear_position": # Convert the transmission gear position from string to integer
                if each_dict.get('value') == "neutral":
                    signal.append(0)
                elif each_dict.get('value') == "first":
                    signal.append(1)
                elif each_dict.get('value') == "second":
                    signal.append(2)
                elif each_dict.get('value') == "third":
                    signal.append(3)
                elif each_dict.get('value') == "fourth":
                    signal.append(4)
            elif each_dict.get('name') == signal_name: 
                signal.append(each_dict.get('value')) # get the list of values for the required signal name.
    return signal


# Get the list of timestamps for the required signal.
#@input - list of dictionaries, signal name
#@return - lists of timestamps
def timestamp_values(ist_from_file, signal_name):
    timestamp = []
    for each_dict in list_from_file: 
        if each_dict.get('name') == signal_name:
            timestamp.append(each_dict.get('timestamp')) # get the timestamp for the required signal name.
    return timestamp


## Calling all the above functions in the required sequence
func0(log_file)
list_from_file = func1(json_file) # Get the list of dictionaries
#func2(list_from_file) # Print the first 10 enteries
func3(list_from_file) # Print all the signal names, take an input from the user and print the number of occurances and value range
#trip_period, trip_distance = func4(list_from_file) # Store the trip period and trip distance
#func6(list_from_file, trip_period, trip_distance) # Compute the max and average speed of the vehicle
func7(list_from_file) # Plot the vehicle path on Google Maps
#func8(list_from_file, trip_distance) # Calculate the mileage of the vehicle using the trip distance and fule used since restart.
func5(list_from_file) # Plot each signal versus timestamp

