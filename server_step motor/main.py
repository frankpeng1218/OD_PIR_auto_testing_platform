


from lib_frank.servo_controller import ServoController
from lib_frank.oled_display import Oled_Display
from lib_frank.sht40_detect import sht40_Detect

import time


global servo_controller

# 賜福馬達控制
servo_controller = ServoController()

servo_controller.set_servo_angle(servo_id = 'servo_1', degree = 0)# 0~90
servo_controller.set_servo_angle(servo_id = 'servo_2', degree = 0)# 0~180
servo_controller.set_servo_angle(servo_id = 'servo_3', degree = 0)# 0~180
servo_controller.set_servo_angle(servo_id = 'servo_4', degree = 0)# 0~180
servo_controller.set_servo_angle(servo_id = 'servo_5', degree = 0)# 0~180
servo_controller.set_servo_angle(servo_id = 'servo_6', degree = 0)# 0~180
# 賜福馬達資訊
current_degrees = servo_controller.get_servo_degrees()
print(current_degrees)

oled = Oled_Display()
sht40 = sht40_Detect()

i = 0
convert = 1
while True:    
    # 溫濕度資訊
    servo_controller.set_servo_angle(servo_id = 'servo_1', degree = i)
    servo_controller.set_servo_angle(servo_id = 'servo_2', degree = i)
    servo_controller.set_servo_angle(servo_id = 'servo_3', degree = i)
    servo_controller.set_servo_angle(servo_id = 'servo_4', degree = i)
    servo_controller.set_servo_angle(servo_id = 'servo_5', degree = i)
    servo_controller.set_servo_angle(servo_id = 'servo_6', degree = i)
    
    sht40_temp_rh = sht40.get_sht40_temp_rh()
    # Olde display
    oled.info_display(temperatrue=sht40_temp_rh['temperature'], humidity=sht40_temp_rh['relative_humidity'],
                      IP_address=1, motor_status=current_degrees)
    
    time.sleep(2)
    i = i + 3*convert
    if i >= 180:
        convert = convert*-1
    if i <= 0:
        convert = convert*-1
        


