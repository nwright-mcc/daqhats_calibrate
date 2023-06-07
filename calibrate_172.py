#!/usr/bin/env python
#
# MCC 172 calibration
#
from datetime import date
import time
import json
import io

# raw_input isn't defined in Python3.x, whereas input wasn't behaving like raw_input in Python 2.x
# this should make both input and raw_input work in Python 2.x/3.x like the raw_input from Python 2.x 
try: input = raw_input
except NameError: raw_input = input
    
# get serial number
serial =  input("Enter serial number: ")

slopes = [0.0, 0.0]
offsets = [0.0, 0.0]

slopes[0] =  float(input("Enter ch 0 slope:  "))
offsets[0] = float(input("Enter ch 0 offset: "))
slopes[1] =  float(input("Enter ch 1 slope:  "))
offsets[1] = float(input("Enter ch 1 offset: "))

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
