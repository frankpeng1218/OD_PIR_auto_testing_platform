
from lib_frank.servo_controller import ServoController
from lib_frank.oled_display import Oled_Display
from lib_frank.sht40_detect import sht40_Detect
from lib_frank.wifi_connect import WiFiManager

import time
import uasyncio as asyncio

global servo_controller

# 賜福馬達控制
servo_controller = ServoController()

# servo_controller.set_servo_angle(servo_id = 'servo_1', degree = 0)# 0~90
# servo_controller.set_servo_angle(servo_id = 'servo_2', degree = 0)# 0~180
# servo_controller.set_servo_angle(servo_id = 'servo_3', degree = 0)# 0~180
# servo_controller.set_servo_angle(servo_id = 'servo_4', degree = 0)# 0~180
# servo_controller.set_servo_angle(servo_id = 'servo_5', degree = 0)# 0~180
# servo_controller.set_servo_angle(servo_id = 'servo_6', degree = 0)# 0~180
# 賜福馬達資訊
current_degrees = servo_controller.get_servo_degrees()
print(current_degrees)

oled = Oled_Display()
sht40 = sht40_Detect()



#WIFI
def check_wifi_status(wlan, led):
    """定期检查WiFi连接状态。"""
    if wlan.isconnected():
        ip_address = wlan.ifconfig()[0]
#         print('WIFI 状态良好，IP地址:', ip_address)
    else:
        print('WIFI 断线')
        led.off()  # 断开连接时熄灭LED
#         asyncio.run(WiFiManager(ssid='dlink-Sales', password='1234567890').connect_to_wifi())  # 尝试重新连接
        asyncio.run(WiFiManager(ssid='frank0820_2.4G', password='jotao1218').connect_to_wifi())  # 尝试重新连接
    time.sleep(1)
    return ip_address

def read_html_file(filename):
    with open(filename, 'r') as file:
        return file.read()

# Load the HTML content from the file
html_template = read_html_file('index.html')

###
# wifi_manager = WiFiManager(ssid='dlink-Sales', password='1234567890')
wifi_manager = WiFiManager(ssid='frank0820_2.4G', password='jotao1218')
asyncio.run(wifi_manager.connect_to_wifi())  # 连接WiFi


check_interval_sec = 0.25


async def serve_client(reader, writer):
    try:
        print("Client connected")
        request_line = await reader.readline()
        print("Request:", request_line)
        # We are not interested in HTTP request headers, skip them
        while await reader.readline() != b"\r\n":
            pass
        
        # find valid commands within the request
        request = str(request_line)
        
        # Check if angle values for each servo are present in the request
        angle_values = {}
        for i in range(1, 7):
            angle_index = request.find(f'angle{i}=')
            if angle_index != -1:
                angle_str = request[angle_index:].split('&')[0].split('=')[1]
                try:
                    angle = int(angle_str)
                    if 0 <= angle <= 180:
                        angle_values[f'servo_{i}'] = angle
                except ValueError:
                    pass
        
        # Set servo angles based on the extracted values
        for servo, angle in angle_values.items():
            if servo == 'servo_1':
                degree = angle
                servo_controller.set_servo_angle(servo_id = 'servo_1', degree = degree)
            elif servo == 'servo_2':
                degree = angle
                servo_controller.set_servo_angle(servo_id = 'servo_2', degree = degree)
            elif servo == 'servo_3':
                degree = angle
                servo_controller.set_servo_angle(servo_id = 'servo_3', degree = degree)
            elif servo == 'servo_4':
                degree = angle
                servo_controller.set_servo_angle(servo_id = 'servo_4', degree = degree)
            elif servo == 'servo_5':
                degree = angle
                servo_controller.set_servo_angle(servo_id = 'servo_5', degree = degree)
            elif servo == 'servo_6':
                degree = angle
                servo_controller.set_servo_angle(servo_id = 'servo_6', degree = degree)
        
        stateis = f"servo_1: {angle_values['servo_1']}, 2: {angle_values['servo_2']}, 3: {angle_values['servo_3']}, 4: {angle_values['servo_4']}, 5: {angle_values['servo_5']}, 6: {angle_values['servo_6']}"
        response = html_template % stateis
        writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        writer.write(response)

        await writer.drain()
        await writer.wait_closed()
    except OSError as e:
        print(f"OSError: {e}")
        await writer.wait_closed()
    except Exception as e:
        print(f"Exception: {e}")
        await writer.wait_closed()
    

async def main():
    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))
    while True:
#         servo_controller.set_servo_angle(servo_id = 'servo_1', degree = degree)
    
        sht40_temp_rh = sht40.get_sht40_temp_rh()
        IP_address = check_wifi_status(wifi_manager.wlan, wifi_manager.led)  # 开始检查WiFi状态
        # Olde display
        oled.info_display(temperatrue=sht40_temp_rh['temperature'], humidity=sht40_temp_rh['relative_humidity'],
                      IP_address=IP_address, motor_status=current_degrees)
        await asyncio.sleep(check_interval_sec)


try:
    asyncio.run(main())  
finally:
    asyncio.new_event_loop()



