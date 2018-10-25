#!/usr/bin/env python
#
# MCC 118 accuracy test
#
import datetime
import time
import json
import sys
import mcc_gpib as gpib
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
board = hats.mcc118(board_num)
print "Serial " + board.serial()
num_channels = board.a_in_num_channels()

# Modify these for the specific test
num_averages = 100
num_points = 10
min_voltage = -10.0
max_voltage = 10.0
output_path = "accuracy_all_{}.csv".format(board_num)

output_file = open(output_path, "w")

str = "Input V (DMM)," + ",".join("Ch {}".format(channel) for channel in range(num_channels)) +  "," + ",".join("Error {}".format(channel) for channel in range(num_channels)) + "\n"
output_file.write(str)

voltage_step = (max_voltage - min_voltage) / (num_points)
voltage_setpoint = min_voltage
point_index = 0

# Set the initial voltage so we don't have a large step
dp8200.set_voltage(voltage_setpoint)
time.sleep(1.0)

while point_index <= num_points:
    print "Point {0} of {1}: ".format(point_index, num_points),
    
    # Set the voltage
    dp8200.set_voltage(voltage_setpoint)

    # allow settling time
    time.sleep(0.1)
    
    # Get the DMM reading 
    dmm_reading = dmm.read_voltage(0)

    # Read the voltages
    count = 0
    sums = [0.0] * board.a_in_num_channels()
    """
    while count < num_averages:
        for channel in range (8):
            value = board.read_voltage(channel, True)
            sums[channel] += value
        count += 1
    """
    for channel in range(8):
        # start the scan
        board.a_in_scan_start(channel_mask = 1 << channel, 
                              samples_per_channel = num_averages,
                              sample_rate_per_channel = 10000)
        # wait for all the data to be returned
        status = board.a_in_scan_read(samples_per_channel = num_averages, 
                                      timeout = 1.0)
        #board.a_in_scan_stop()
        board.a_in_scan_cleanup()
        
        if len(status['data']) != num_averages:
            print("Did not receive all the data.")
            output_file.close()
            dp8200.set_voltage(0.0)
            sys.exit(1)
        
        for x in range(num_averages):
            sums[channel] += status['data'][x]
            
    averages = [x / num_averages for x in sums]
    errors = [(x - dmm_reading) for x in averages]

    s = ""
    for channel in range(8):
        if abs(errors[channel]) > 0.01:
            s += "\033[1;31;40m{0:6.3f}\033[1;37;40m ".format(errors[channel])
        else:
            s += "{0:6.3f} ".format(errors[channel])    
    print s
    #print "".join("{0:6.3f} ".format(x) for x in errors)

    s = "{0:.6f},".format(dmm_reading)
    s += "".join("{0:.6f},".format(x) for x in averages)
    s += "".join("{0:.6f},".format(x) for x in errors)
    s += "\n"
    output_file.write(s)
    point_index += 1
    voltage_setpoint += voltage_step

output_file.close()
dp8200.set_voltage(0.0)
