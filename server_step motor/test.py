# 导入ServoController类
from lib_frank.servo_controller import ServoController
from lib_frank.oled_display import Oled_Display

# 创建ServoController实例
global servo_controller
servo_controller = ServoController()

servo_controller.set_servo_angle(servo_id = 'servo_1', degree = 5.1)
# servo_controller.set_servo_angle(servo_id = 'servo_2', degree = 0)
# servo_controller.set_servo_angle(servo_id = 'servo_3', degree = 0)
# servo_controller.set_servo_angle(servo_id = 'servo_4', degree = 0)
# servo_controller.set_servo_angle(servo_id = 'servo_5', degree = 0)
# servo_controller.set_servo_angle(servo_id = 'servo_6', degree = 0)
# 获取当前各伺服电机的角度
current_degrees = servo_controller.get_servo_degrees()
print(current_degrees)


oled_info = Oled_Display()
oled_info.info_display(temperatrue=1, humidity=1, IP_address=1, motor_status=current_degrees)