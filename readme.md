# Instructions

## MCC 118
   ### Creating an EEPROM image:

   1. The specific device must be calibrated (you can use calibrate_118.py as an example for 
      calibration code) and the calibration file calibrate.txt created.  It must contain a JSON structure
      with the serial number, calibration date, and calibration coefficients.
   2. Run **make_118_eeprom.sh** to create the EEPROM image eeprom.eep.  This image is specific to the 
      current board being configured - each board will have unique EEPROM contents.
   3. Run **sudo program_eeprom.sh** to write the EEPROM to the MCC 118.  The EEPROM write header mush be 
      shorted during the write.

   ### Making changes to the configuration:
   The device tree overlay, MCC_118.dtbo, was created from compiling MCC_118-overlay.dts using 
   standard device tree tools:

   ```sh
   dtc -@ -I dts -O dtb -o MCC_118.dtbo MCC_118-overlay.dts
   ```
   The file MCC_118_eeprom.txt is the Raspberry Pi HAT EEPROM description file that has already
   been created with the correct settings.

## MCC 152
   ### Creating an EEPROM image:

   3. The specific device must be serialized (you can use calibrate_152.py as an example for 
      serialization code) and the calibration file calibrate.txt created.  It must contain a JSON structure
      with the serial number.
   4. Run **make_152_eeprom.sh** to create the EEPROM image eeprom.eep.  This image is specific to the 
      current board being configured - each board will have unique EEPROM contents.
   5. Run **sudo program_eeprom.sh** to write the EEPROM to the MCC 152.  The EEPROM write header mush be 
      shorted during the write.

   ### Making changes to the configuration:
   The device tree overlay, MCC_152.dtbo, was created from compiling MCC_152-overlay.dts using 
   standard device tree tools:

   ```sh
   dtc -@ -I dts -O dtb -o MCC_152.dtbo MCC_152-overlay.dts
   ```
   The file MCC_152_eeprom.txt is the Raspberry Pi HAT EEPROM description file that has already
   been created with the correct settings.
