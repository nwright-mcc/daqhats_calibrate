#!/usr/bin/env python
#
# MCC 134 calibration
#
from datetime import date
import time
import datetime
import json
import io

# get serial number
serial = raw_input("Enter serial number: ")

num_channels = 4
slopes = [0.0] * num_channels
offsets = [0.0] * num_channels

print ""

for channel in range(num_channels):
    slopes[channel] =  float(raw_input("Enter ch {} slope:  ".format(channel)))
    offsets[channel] = float(raw_input("Enter ch {} offset: ".format(channel)))
    print ""

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
