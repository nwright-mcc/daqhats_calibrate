To create an EEPROM image for an MCC 118:

1. The device tree overlay, MCC_118.dtbo, wass created from compiling MCC_118-overlay.dts using 
standard device tree tools: dtc -@ -I dts -O dtb -o MCC_118.dtbo MCC_152-overlay.dts
2. The file MCC_118_eeprom.txt is the Raspberry Pi HAT EEPROM description file that has already
been created with the correct settings.
3. The specific device must be calibrated (you can use calibrate_118.py as an example for 
calibration code) and the calibration file calibrate.txt created.  It must contain a JSON structure
with the serial number, calibration date, and calibration coefficients.
4. Run make_118_eeprom.sh to create the EEPROM image eeprom.eep.  This image is specific to the 
current board being configured - each board will have unique EEPROM contents.
5. Run program_eeprom.sh to write the EEPROM to the MCC 118.  The EEPROM write header mush be 
shorted during the write.

