#!/usr/bin/env python
#
# MCC 134 accuracy test
#
import datetime
import time
import json
import sys
import MCC_GPIB_Library as gpib
import mcchats as hats

print datetime.datetime.now()

# Create the DMM instrument
dmm = gpib.DMM()
# Create the DP8200 instrument
dp8200 = gpib.DP8200()

if len(sys.argv) > 1:
    # get board address
    board_num = int(sys.argv[1])
else:
    board_num = 0

# Create an instance of the board
board = hats.mcc134(board_num)
print "Serial " + board.serial()
num_channels = board.a_in_num_channels()

print("Initializing...")

# Modify these for the specific test
num_averages = 80
num_points = 10
min_voltage = -0.070
max_voltage = 0.070

output_file2 = open("test_data.csv", "w")


voltage_step = (max_voltage - min_voltage) / (num_points)
voltage_setpoint = min_voltage
point_index = 0

# Set the initial voltage so we don't have a large step
dp8200.set_voltage(voltage_setpoint)
#time.sleep(1.0)

print("{} Points".format(num_points))
print("Errors in uV")
print("Point #\t  milliVolts\t  Error 0\t  Error 1\t  Error 2\t  Error 3".format(num_points + 1))
while point_index <= num_points:
    # Set the voltage
    dp8200.set_voltage(voltage_setpoint)

    # allow settling time
    time.sleep(5)
    
    # Get the DMM reading 
    #dmm_reading = dmm.read_voltage(1)

    # Read the voltages
    count = 0
    sums = [0.0] * num_channels

    for sample in range(num_averages):
        value = board.a_in_read(0)
        print("{:7.4f}".format(value*1e3))
        output_file2.write("{:7.4f}\n".format(value*1e3))
    output_file2.write("\n")
    
    point_index += 1
    voltage_setpoint += voltage_step

output_file2.close()
dp8200.set_voltage(0.0)
