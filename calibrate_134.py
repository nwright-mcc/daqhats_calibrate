#!/usr/bin/env python
#
# MCC 134 calibration
#
from datetime import date
import time
import datetime
import json
import io
import MCC_GPIB_Library as gpib
import mcchats as hats

# get address
print datetime.datetime.now()

address = raw_input("Enter board address: ")

# get serial number
serial = raw_input("Enter serial number: ")

num_channels = 4
slopes = [0.0] * num_channels
offsets = [0.0] * num_channels
lsb_size = 2 * 0.128 / (2 ** 24)
#zero_code = 2048

print("Initializing...")

# Create the DMM instrument
dmm = gpib.DMM()
# Create the DP8200 instrument
dp8200 = gpib.DP8200()

# Create an instance of the board
board = hats.mcc134(int(address))

num_averages = 40
num_points = 3
min_voltage = -0.070
max_voltage = 0.070
output_path = "calibrate_134.csv"
voltage_step = (max_voltage - min_voltage) / (num_points - 1)

output_file = open(output_path, "w")
str = datetime.datetime.now().isoformat() + "\n"
output_file.write(str)
str = "Input V (DMM), " + ", ".join("Ch {}".format(x) for x in range(num_channels)) + "\n"
output_file.write(str)

voltage_setpoint = min_voltage

# Set the initial voltage so we don't have a large step
dp8200.set_voltage(voltage_setpoint)
time.sleep(3)

codes_buffer = []
desired = []

print("Calibrating...")
point_index = 0
while point_index < num_points:
    print "Point {0} of {1}: set {2:.3f} mV".format(point_index + 1, num_points, voltage_setpoint * 1e3)

    # Set the voltage
    dp8200.set_voltage(voltage_setpoint)

    time.sleep(6)

    # Get the DMM reading
    dmm_reading = dmm.read_voltage(1)
    print("  DMM read {:.3f} mV".format(dmm_reading * 1e3))
    dmm_code = (dmm_reading / lsb_size) #+ zero_code
    desired.append(dmm_code)
    #print("Desired {}".format(dmm_code))

    # Read the ADC inputs
    count = 0
    averages = [0.0] * num_channels
    
    for channel in range(num_channels):
        for sample in range(num_averages):
            value = board.a_in_read(channel, scaled = False, calibrated = False)
            #print("Ch {0} read {1}".format(channel, value))
            averages[channel] += value/num_averages

    print("  ADC read {:.3f} mV".format(averages[0] * lsb_size * 1e3))
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

print
print "Channel\tSlope\tOffset"
print "-------\t------\t-------"
for channel in range(num_channels):
    print "{0}\t{1:.9f}\t{2:.3f}".format(channel, slopes[channel], offsets[channel])
print

dp8200.set_voltage(0.0)
output_file.close()

# Create calibration file
data = {}
data['serial'] = serial
data['calibration'] = {}
data['calibration']['date'] = date.today().isoformat()
data['calibration']['slopes'] = slopes
data['calibration']['offsets'] = offsets
#hat_data = json.dumps(data, indent=0, separators=(',', ':'), ensure_ascii=False)
hat_data = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
with io.open("./calibrate_134.txt", "w", encoding="utf8") as outfile:
    outfile.write(unicode(hat_data))

print("Output saved in calibrate_134.txt.")
