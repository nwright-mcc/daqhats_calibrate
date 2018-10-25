#!/bin/sh
sudo eepromutils/eepflash.sh -t=24c32 -w -f=eeprom.eep
sudo eepromutils/eepflash.sh -t=24c32 -r -f=readback.eep
length=$(wc -c < eeprom.eep)
cmp -n $length eeprom.eep readback.eep
if [ $? -eq 1 ]; then
    echo "EEPROM content mismatch; is the write enable jumper in place?"
    exit 1
fi
echo "Success"
exit 0
