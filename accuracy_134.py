#!/usr/bin/env python
#
# MCC 134 accuracy test
#
import datetime
import time
import json
import sys
import MCC_GPIB_Library as gpib
import daqhats as hats

channels = [0, 1, 2, 3]

print datetime.datetime.now()

# Create the DMM instrument
dmm = gpib.DMM()
# Create the DP8200 instrument
dp8200 = gpib.DP8200()

# drive to 0V during initialization in order to settle analog inputs
dp8200.set_voltage(0)

if len(sys.argv) > 1:
    # get board address
    board_num = int(sys.argv[1])
else:
    board_num = 0

# Create an instance of the board
board = hats.mcc134(board_num)
print "Serial " + board.serial()
num_channels = len(channels) #board.info().NUM_AI_CHANNELS

# display the cal coefficients

for channel in channels: #range(num_channels):
    coef = board.calibration_coefficient_read(channel)
    #print(coef)
    print("  Ch {0} slope: {1} offset: {2}".format(channel, coef.slope, coef.offset))

print("Initializing...")

# Modify these for the specific test
num_averages = 20
num_points = 14
min_voltage = -0.070
max_voltage = 0.070
output_path = "accuracy_134_{}.csv".format(board_num)

output_file = open(output_path, "w")

output_file2 = open("test_data.csv", "w")

str = "Input V (DMM)," + ",".join("Ch {}".format(channel) for channel in channels) +  "," + ",".join("Error {}".format(channel) for channel in channels) + "\n"
output_file.write(str)

voltage_step = (max_voltage - min_voltage) / (num_points)
voltage_setpoint = min_voltage
point_index = 0

# Set the initial voltage so we don't have a large step
dp8200.set_voltage(voltage_setpoint)
time.sleep(3)

print("{} Points".format(num_points))
print("Errors in uV")
print("Point #\t  milliVolts\t  " + "\t  ".join("Error {}".format(channel) for channel in channels))
while point_index <= num_points:
    # Set the voltage
    dp8200.set_voltage(voltage_setpoint)

    # allow settling time
    time.sleep(1)
    
    # Get the DMM reading 
    dmm_reading = dmm.read_voltage(1)

    # Read the voltages
    count = 0
    sums = [0.0] * num_channels
    index = 0
    for channel in channels:
        for sample in range(num_averages):
            value = board.a_in_read(channel)
            output_file2.write("{:7.4f}\n".format(value*1e3))
            sums[index] += value
        index += 1
        output_file2.write("\n")

    output_file2.write("\n")
    
    averages = [x / num_averages for x in sums]
    errors = [(x - dmm_reading) for x in averages]

    s = "   {0}\t  {1:7.4f}\t".format(point_index + 1, dmm_reading*1e3)
    index = 0
    for channel in channels:
        if abs(errors[index]*1e6) > 3:
            s += "  \033[1;31;40m{0:7.4f}\033[1;37;40m\t".format(errors[index]*1e6)
        elif abs(errors[index]*1e6) >= 2:
            s += "  \033[1;33;40m{0:7.4f}\033[1;37;40m\t".format(errors[index]*1e6)
        else:
            s += "  {0:7.4f}\t".format(errors[index]*1e6)    
        index += 1
    print s
    #print "".join("{0:6.3f} ".format(x) for x in errors)

    s = "{0:.6f},".format(dmm_reading*1e3)
    s += "".join("{0:.6f},".format(x*1e3) for x in averages)
    s += "".join("{0:.6f},".format(x*1e6) for x in errors)
    s += "\n"
    output_file.write(s)
    point_index += 1
    voltage_setpoint += voltage_step

output_file.close()
output_file2.close()
dp8200.set_voltage(0.0)
