#Frank_edited_0416

import time
import network
import uasyncio as asyncio
from machine import Pin
from servo import Servo

#----------------------------general----------------------------
led = Pin("LED", Pin.OUT, value=1)
#----------------------------general----------------------------

#----------------------------servo motor----------------------------
my_servo_1 = Servo(pin_id=1)
my_servo_2 = Servo(pin_id=2)
my_servo_3 = Servo(pin_id=3)
my_servo_4 = Servo(pin_id=4)
my_servo_5 = Servo(pin_id=5)
my_servo_6 = Servo(pin_id=6)
global servo_degree_1, servo_degree_2, servo_degree_3, servo_degree_4, servo_degree_5, servo_degree_6
servo_degree_1 = 0
servo_degree_2 = 0
servo_degree_3 = 0
servo_degree_4 = 0
servo_degree_5 = 0
servo_degree_6 = 0
my_servo_1.write(servo_degree_1)
my_servo_2.write(servo_degree_2)
my_servo_3.write(servo_degree_3)
my_servo_4.write(servo_degree_4)
my_servo_5.write(servo_degree_5)
my_servo_6.write(servo_degree_6)
#----------------------------servo motor----------------------------

#--------------Configure your WiFi SSID and password--------------
ssid = 'dlink-Sales'
password = '1234567890'
check_interval_sec = 0.25
wlan = network.WLAN(network.STA_IF)
#--------------Configure your WiFi SSID and password--------------


#------------------------------general def------------------------------
def toggle_led(led):
    led.toggle()

def blink_led(frequency=0.5, num_blinks=3):
    for _ in range(num_blinks):
        led.on()
        time.sleep(frequency)
        led.off()
        time.sleep(frequency)
#------------------------------general def------------------------------

#------------------------------servo motor def------------------------------
def servo_move_1(degree):
    my_servo_1.write(degree)
def servo_move_2(degree):
    my_servo_2.write(degree)
def servo_move_3(degree):
    my_servo_3.write(degree)
def servo_move_4(degree):
    my_servo_4.write(degree)
def servo_move_5(degree):
    my_servo_5.write(degree)
def servo_move_6(degree):
    my_servo_6.write(degree)
#------------------------------servo motor def------------------------------

import time

# 定义每次移动的角度增量
step = 6

# 初始化当前角度
current_degree = 0
servo_move_1(current_degree)
servo_move_2(current_degree)
servo_move_3(current_degree)
servo_move_4(current_degree)
servo_move_5(current_degree)
servo_move_6(current_degree)
# 定义移动方向，1表示向前，-1表示向后
direction = 1

# 无限循环，让servo持续移动
while True:
    # 移动servo到当前角度
    servo_move_1(current_degree)
    servo_move_2(current_degree)
    servo_move_3(current_degree)
    servo_move_4(current_degree)
    servo_move_5(current_degree)
    servo_move_6(current_degree)
    
    # 延时一段时间
    time.sleep(1)
    
    # 更新当前角度
    current_degree += step * direction
    
    # 如果到达边界，改变移动方向
    if current_degree >= 180 or current_degree <= 0:
        direction *= -1

