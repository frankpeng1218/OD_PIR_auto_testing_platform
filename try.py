import time
import network
import uasyncio as asyncio
from machine import Pin
from servo import Servo

#----------------------------general----------------------------
led = Pin("LED", Pin.OUT, value=1)
#----------------------------general----------------------------

#----------------------------servo motor----------------------------
my_servo_0 = Servo(pin_id=1)
my_servo_1 = Servo(pin_id=1)
my_servo_2 = Servo(pin_id=2)
my_servo_3 = Servo(pin_id=3)
my_servo_4 = Servo(pin_id=4)
my_servo_5 = Servo(pin_id=5)
my_servo_6 = Servo(pin_id=6)
my_servo_1.write(120)

def set_servo_angle(servo_id, angle):
    if 0 <= angle <= 180:
        servos[servo_id - 1].write(angle)
        servo_degrees[servo_id - 1] = angle
        print(f"Set servo {servo_id} angle to {angle} degrees")
    else:
        print("Invalid angle value")

#set_servo_angle(1, 0)
#set_servo_angle(2, 0)
#set_servo_angle(3, 0)
#set_servo_angle(4, 0)
#set_servo_angle(5, 0)
#set_servo_angle(6, 0)
        
        