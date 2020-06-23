#!/usr/bin/env python
#
# MCC 128 calibration
#
from datetime import date
import time
import json
import io

# get serial number
serial =  raw_input("Enter serial number: ")

num_ranges = 4
slopes = [1.0] * num_ranges
offsets = [0.0] * num_ranges

slopes[0] =  float(raw_input("Enter 10V slope:  "))
offsets[0] = float(raw_input("Enter 10V offset: "))
slopes[1] =  float(raw_input("Enter 5V slope:   "))
offsets[1] = float(raw_input("Enter 5V offset:  "))
slopes[2] =  float(raw_input("Enter 2V slope:   "))
offsets[2] = float(raw_input("Enter 2V offset:  "))
slopes[3] =  float(raw_input("Enter 1V slope:   "))
offsets[3] = float(raw_input("Enter 1V offset:  "))

# Create calibration file
data = {}
data['serial'] = serial
data['calibration'] = {}
data['calibration']['date'] = date.today().isoformat()
data['calibration']['slopes'] = slopes
data['calibration']['offsets'] = offsets

hat_data = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
with io.open("./calibrate_128.txt", "w", encoding="utf8") as outfile:
    outfile.write(unicode(hat_data))

print("Output saved in calibrate_128.txt.")
