#!/usr/bin/env python
#
# MCC 152 setup
#
import json
import io

# get serial number
serial = raw_input("Enter serial number: ")

# Create serial file
data = {}
data['serial'] = serial
hat_data = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
with io.open("./serial_152.txt", "w", encoding="utf8") as outfile:
    outfile.write(unicode(hat_data))

print("Output saved in serial_152.txt.")
