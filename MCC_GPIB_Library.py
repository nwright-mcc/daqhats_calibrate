#
# Measurement Computing GPIB instrument library
#
import time
import Gpib

#******************************************************************************
# HP 34401A DMM
class DMM:

    def __init__(self):
        self.device = Gpib.Gpib(0, 5)
        # first write after reboot fails so add a retry mechanism
        self.device.timeout(9)	# 100 ms
        written = False
        while not written:
            try:
                self.device.write("*CLS")
            except:
                pass
            else:
                written = True
                self.device.timeout(13)
        
        self.device.write("INP:IMP:AUTO ON")
        self.device.write("CONF:VOLT:DC")
        return
    
    def __del__(self):
        self.device.ibloc()
        
    def read_voltage(self, resolution):
        if resolution == 0:
            self.device.write(":MEAS:VOLT:DC? DEF,DEF")
        else:
            self.device.write(":MEAS:VOLT:DC? DEF,MIN")
        
        result = self.device.read()
        
        value = float(result)
        return value
    
    def display(self, string):
        self.device.write("DISP:TEXT \"{0:s}\"".format(string))
        return
        
#******************************************************************************
# DataPrecision 8200 calbrator
class DP8200:

    def __init__(self):
        self.device = Gpib.Gpib(0, 20)

        # first write after reboot fails so add a retry mechanism
        self.device.timeout(9)	# 100 ms
        written = False
        while not written:
            try:
                self.device.write("L")
            except:
                pass
            else:
                written = True
                self.device.timeout(13)
        return
    
    def __del__(self):
        self.device.write("L")
        return
        
    def set_voltage(self, voltage):
        if abs(voltage) > 100.0:
            intval = int(round(voltage*1000, 0))
            string = "V3{0:+08d}".format(intval)
        elif abs(voltage) > 10.0:
            intval = int(round(voltage*10000, 0))
            string = "V2{0:+08d}".format(intval)
        else:
            intval = int(round(voltage*100000, 0))
            string = "V1{0:+08d}".format(intval)

        self.device.write(string)
        return
