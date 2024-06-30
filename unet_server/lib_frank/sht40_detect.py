from lib_frank.sht4x import SHT4X
from machine import Pin, I2C

class sht40_Detect:
    def __init__(self):
        self.i2c = I2C(1, sda=Pin(14), scl=Pin(15), freq=400000)  # RP2040 的正確 I2C pin
        self.sht = SHT4X(i2c=self.i2c, address=0x44)
        self.sht40_temp_rh = {
            'temperature': 0,
            'relative_humidity': 0,
        }
    def get_sht40_temp_rh(self):
        temperature, relative_humidity = self.sht.measurements
        self.sht40_temp_rh['temperature'] = temperature
        self.sht40_temp_rh['relative_humidity'] = relative_humidity
        return self.sht40_temp_rh
    



