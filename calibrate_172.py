#!/usr/bin/env python
#
# MCC 172 calibration
#
from datetime import date
import time
import json
import io
import sys

# Fix unicode and raw_input changes in Python 3
if sys.version_info[0] >= 3:
    unicode = str
    raw_input = input
    
# get serial number
serial =  raw_input("Enter serial number: ")

slopes = [0.0, 0.0]
offsets = [0.0, 0.0]

slopes[0] =  float(raw_input("Enter ch 0 slope:  "))
offsets[0] = float(raw_input("Enter ch 0 offset: "))
slopes[1] =  float(raw_input("Enter ch 1 slope:  "))
offsets[1] = float(raw_input("Enter ch 1 offset: "))

# Create calibration file
data = {}
data['serial'] = serial
data['calibration'] = {}
data['calibration']['date'] = date.today().isoformat()
data['calibration']['slopes'] = slopes
data['calibration']['offsets'] = offsets
#hat_data = json.dumps(data, indent=0, separators=(',', ':'), ensure_ascii=False)
hat_data = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
with io.open("./calibrate_172.txt", "w", encoding="utf8") as outfile:
    outfile.write(unicode(hat_data))

print("Output saved in calibrate_172.txt.")
