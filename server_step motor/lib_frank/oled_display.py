from lib_frank.ssd1306 import SSD1306_I2C
from machine import Pin, I2C

class Oled_Display:
    def __init__(self):
        self.i2c = I2C(1, sda=Pin(14), scl=Pin(15), freq=400000)  # RP2040 的正確 I2C pin
        self.oled = SSD1306_I2C(width=128, height=64, i2c=self.i2c, addr=0x3C)

    def info_display(self, temperatrue, humidity, IP_address, motor_status):

        self.oled.fill(0)
        self.oled.text(f"{IP_address} ", 0, 0)
        self.oled.text(f"Temp :{temperatrue:.2f} C", 0, 10)
        self.oled.text(f"Humid:{humidity:.2f} %", 0, 20)
        self.oled.text(f"S1:{motor_status['servo_1']} ", 0, 30)
        self.oled.text(f"S2:{motor_status['servo_2']} ", 60, 30)
        self.oled.text(f"S3:{motor_status['servo_3']} ", 0, 40)
        self.oled.text(f"S4:{motor_status['servo_4']} ", 60, 40)
        self.oled.text(f"S5:{motor_status['servo_5']} ", 0, 50)
        self.oled.text(f"S6:{motor_status['servo_6']} ", 60, 50)
        self.oled.show()
  
# a =  Oled_Display()
# while True:
#     b = a.info_display(1,1,1,1)
#     print(123)

