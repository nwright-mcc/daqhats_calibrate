#!/usr/bin/env python3
#
# MCC 118 calibration
#
from datetime import date
import time
import json
import io
#import MCC_GPIB_Library as gpib
import daqhats as hats

# get address
address = int(input("Enter board address: "))
print(address)

# get serial number
serial = input("Enter serial number: ")
print(serial)

num_channels = 8
slopes = [0.0] * num_channels
offsets = [0.0] * num_channels
lsb_size = 20.0 / 4096.0
zero_code = 2048

print("Initializing...")

# Create the DMM instrument
#dmm = gpib.DMM()
# Create the DP8200 instrument
#dp8200 = gpib.DP8200()

# ToDo: Initialize your DMM and precision voltage source here

# Create an instance of the board
board = hats.mcc118(address)

num_averages = 1000
num_points = 3
min_voltage = -10.0
max_voltage = 10.0
output_path = "calibrate_118.csv"
voltage_step = (max_voltage - min_voltage) / (num_points - 1)

output_file = open(output_path, "w")
str = "Input V (DMM), " + ", ".join("Ch {}".format(x) for x in range(num_channels)) + "\n"
output_file.write(str)

voltage_setpoint = min_voltage

# ToDo: Set the initial voltage on the voltage source so we don't have a large step
#dp8200.set_voltage(voltage_setpoint)

time.sleep(1.0)

codes_buffer = []
desired = []

print("Calibrating...")
point_index = 0
dmm_reading = 0
while point_index < num_points:
    #print "Point {0} of {1}: ".format(point_index, num_points),

    # ToDo: Set the voltage on the precision source
    #dp8200.set_voltage(voltage_setpoint)

    time.sleep(1)

    # ToDo: Get the DMM reading
    #dmm_reading = dmm.read_voltage(0)
    dmm_code = (dmm_reading / lsb_size) + zero_code
    desired.append(dmm_code)

    # Read the voltages
    count = 0
    sums = [0.0] * num_channels
    """
    while count < num_averages:
        for channel in range (num_channels):
            value = board.read_code(channel, False)
            sums[channel] += value
        count += 1
    """
    for channel in range(num_channels):
        # start a scan on the channel
        board.a_in_scan_start(channel_mask = 1 << channel,
            samples_per_channel = num_averages,
            sample_rate_per_channel = 10000,
            options = hats.OptionFlags.NOSCALEDATA | hats.OptionFlags.NOCALIBRATEDATA)
        # perform a blocking read of all the data
        result = board.a_in_scan_read(samples_per_channel = num_averages, timeout = 1.0)
        board.a_in_scan_cleanup()
        if len(result.data) != num_averages:
            raise ValueError("Incorrect number of samples read")

        for sample in result.data:
            sums[channel] += sample

    averages = [x / num_averages for x in sums]
    str = "{0:.6f},".format(dmm_reading)
    str += ",".join("{0:.6f}".format(x) for x in averages)
    str += "\n"
    output_file.write(str)

    codes_buffer.append(averages)

    point_index += 1
    voltage_setpoint += voltage_step

output_file.write("\n")

# calculate linear regression for each channel
for channel in range(num_channels):
    sum_x = 0.0
    sum_y = 0.0
    sum_x2 = 0.0
    sum_xy = 0.0

    for point in range(num_points):
        sum_x += codes_buffer[point][channel]
        sum_y += desired[point]
        sum_xy += codes_buffer[point][channel] * desired[point]
        sum_x2 += codes_buffer[point][channel] * codes_buffer[point][channel]

    slopes[channel] = ((num_points * sum_xy) - (sum_x * sum_y)) / ((num_points * sum_x2) - (sum_x * sum_x))
    offsets[channel] = (sum_y / num_points) - slopes[channel] * (sum_x / num_points)

    s = "Ch {0:d} Slope,{1:.9f}\nCh {2:d} Offset,{3:.9f}\n".format(channel, slopes[channel], channel, offsets[channel])
    output_file.write(s)

print()
print("Channel\tSlope\tOffset")
print("-------\t------\t-------")
for channel in range(8):
    print("{0}\t{1:.3f}\t{2:.3f}".format(channel, slopes[channel], offsets[channel]))
print()

# ToDo: set the precision supply to 0V output
#dp8200.set_voltage(0.0)
output_file.close()

# Create calibration file
data = {}
data['serial'] = serial
data['calibration'] = {}
data['calibration']['date'] = date.today().isoformat()
data['calibration']['slopes'] = slopes
data['calibration']['offsets'] = offsets
hat_data = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
with io.open("./calibrate_118.txt", "w", encoding="utf8") as outfile:
    outfile.write(hat_data)

print("Output saved in calibrate_118.txt.")
