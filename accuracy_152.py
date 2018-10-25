#!/usr/bin/env python
#
# MCC 152 analog output accuracy test
#
import datetime
import time
import json
import sys
import MCC_GPIB_Library as gpib
import daqhats as hats

print datetime.datetime.now()

# Create the DMM instrument
dmm = gpib.DMM()

if len(sys.argv) > 2:
    # get board address
    board_num = int(sys.argv[1])
    channel = int(sys.argv[2])
else:
    board_num = 0
    channel = 0

# Create an instance of the board
board = hats.mcc152(board_num)
print "Serial " + board.serial()

# Check the offset error at the top of the zero-scale error region
board.a_out_write(channel, 0.010)
time.sleep(0.1)
dmm_reading = dmm.read_voltage(0)
error = dmm_reading - 0.010
print("Offset error:   {:6.3f} mV".format(error * 1000))
print

# Modify these for the specific test
num_points = 10
min_voltage = 0.0
max_voltage = 5.0
output_path = "accuracy_152_{0}_{1}.csv".format(board_num, channel)

output_file = open(output_path, "w")

str = "Set V,Output V,Error (mV)\n"
output_file.write(str)

voltage_step = (max_voltage - min_voltage) / (num_points)
voltage_setpoint = min_voltage
point_index = 0

# Set the initial voltage so we don't have a large step
board.a_out_write(channel, voltage_setpoint)
time.sleep(0.1)

while point_index <= num_points:
    print "Point {0} of {1}: ".format(point_index, num_points),
    
    # Set the voltage
    board.a_out_write(channel, voltage_setpoint)

    # allow settling time
    time.sleep(0.1)
    
    # Get the DMM reading 
    dmm_reading = dmm.read_voltage(0)

    error = (dmm_reading - voltage_setpoint) * 1000

    s = ""
    if abs(error) > 45.0:
        s += "\033[1;31;40m{0:6.3f}\033[1;37;40m mV".format(error)
    else:
        s += "{0:6.3f} mV".format(error)    
    print s

    s = "{0:.6f},{1:.6f},{2:.6f}\n".format(voltage_setpoint, dmm_reading, error)
    output_file.write(s)
    point_index += 1
    voltage_setpoint += voltage_step

output_file.close()

board.a_out_write(channel, 0.0)
