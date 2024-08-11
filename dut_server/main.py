from lib_frank.servo_controller import ServoController
from lib_frank.oled_display import Oled_Display
# from lib_frank.sht40_detect import sht40_Detect
from lib_frank.wifi_connect import WiFiManager
import time
import uasyncio as asyncio
from phew import server
import json
import urequests as requests
from machine import Pin, Timer

global servo_controller

with open('configuration.txt', 'r') as file:
    lines = file.readlines()
header = lines[0].strip().split() 
data = lines[1].strip().split()    
config = dict(zip(header, data))


url_detection = f"http://{config['master_server_ip']}:{config['port']}/detection"


# 設置GP16為輸入引腳，並啟用上拉電阻
gp16 = Pin(16, Pin.IN, Pin.PULL_UP)

# 初始化計時器和計時器標誌
timer = Timer()
debounce_flag = False

# 定義一個回調函數，當GP16變為低電平時執行
def handle_interrupt(pin):
    global debounce_flag
    if pin.value() == 0 and not debounce_flag:
        print('detected')
        #-----
        while True:
            try:
                
                payload = {'name': 'dut_server', 'detected': True}
                headers = {'Content-Type': 'application/json', 'Authorization': 'None'}

                response = requests.post(url_detection, json=payload, headers=headers)
                print("Response:", response.text)
                if response.status_code == 200:
                    response_data = response.json()
                    if response_data.get("message") == "detection received":
                        print("detection received")
                        break  # Exit the loop if successful
                    else:
                        print("Server response:", response_data.get("message"))
                else:
                    print("Failed")


            except OSError as e:
                print(f"OS error occurred: {e}")
                print("Retrying...")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                print("Retrying...")
            
                break  # Exit the loop on unexpected errors
        #-----
        debounce_flag = True
        # 啟動計時器，3秒後重置防彈跳標誌
        timer.init(mode=Timer.ONE_SHOT, period=500, callback=reset_debounce_flag)

# 重置防彈跳標誌的函數
def reset_debounce_flag(timer):
    global debounce_flag
    debounce_flag = False

# 配置中斷，觸發方式為下降沿（從高電平到低電平）
gp16.irq(trigger=Pin.IRQ_FALLING, handler=handle_interrupt)




def check_wifi_status(wlan, led):
    if wlan.isconnected():
        ip_address = wlan.ifconfig()[0]
    else:
        print('WIFI 断线')
        led.off()
        asyncio.run(wifi_manager.connect_to_wifi())
    time.sleep(1)
    return ip_address

        
        

# Initialize components
servo_controller = ServoController()
oled = Oled_Display()
# sht40 = sht40_Detect()




# WiFi setup
wifi_manager = WiFiManager(ssid=config['ssid'], password=config['password'])
asyncio.run(wifi_manager.connect_to_wifi())
check_interval_sec = 0.25

url = f"http://{config['master_server_ip']}:{config['port']}/receive_ip"
count = 0

while True:
    try:
        
        dut_server_ip = check_wifi_status(wifi_manager.wlan, wifi_manager.led)
        payload = {'name': 'dut_server','ip_address': dut_server_ip}
        headers = {'Content-Type': 'application/json', 'Authorization': 'None'}

        
        oled.oled.fill(0)
        oled.oled.text(f'{dut_server_ip}', 0, 0)
        oled.oled.text(f'Connecting to', 0, 15)
        oled.oled.text(f'master server', 0, 25)
        oled.oled.text(f'{config['master_server_ip']}', 0, 35)
        oled.oled.text(f':{config['port']}', 0, 45)
        oled.oled.text(f'retry:{count}', 0, 55)
        oled.oled.show()

        response = requests.post(url, json=payload, headers=headers)
        print("Response:", response.text)
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get("message") == "IP address received successfully":
                print("IP address sent successfully to server")
                break  # Exit the loop if successful
            else:
                print("Server response:", response_data.get("message"))
        else:
            print("Failed to send IP address. Retrying...")



    except OSError as e:
        print(f"OS error occurred: {e}")
        print("Retrying...")
        
        oled.oled.fill(0)
        oled.oled.text(f'{dut_server_ip}', 0, 0)
        oled.oled.text(f'Connecting to', 0, 15)
        oled.oled.text(f'master server', 0, 25)
        oled.oled.text(f'{config['master_server_ip']}', 0, 35)
        oled.oled.text(f':{config['port']}', 0, 45)
        oled.oled.text(f'retry:{count}', 0, 55)
        oled.oled.show()
        count = count + 1
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print("Retrying...")
        
        oled.oled.fill(0)
        oled.oled.text(f'{dut_server_ip}', 0, 0)
        oled.oled.text(f'Connecting to', 0, 15)
        oled.oled.text(f'master server', 0, 25)
        oled.oled.text(f'{config['master_server_ip']}', 0, 35)
        oled.oled.text(f':{config['port']}', 0, 45)
        oled.oled.text(f'retry:{count}', 0, 55)
        oled.oled.show()
        count = count + 1
        break  # Exit the loop on unexpected errors

oled.oled.fill(0)
oled.oled.text(f'dut_server:', 0, 0)
oled.oled.text(f'{dut_server_ip}', 0, 10)
oled.oled.text(f'Waiting for cmd', 0, 20)
oled.oled.show()



# Define API route for setting servo angles
@server.route("/set_servo", methods=["POST"])
def set_servo(request):
    params = request.query_string
    print('params:',params)
    pairs = params.split('&')
    servo_dict = {}
    for pair in pairs:
        key, value = pair.split('=')
        servo_dict[key] = value
    print('-------')
    print('servo_dict:',servo_dict)
    for servo, angle in servo_dict.items():
        if servo == 'servo_1':
            degree = angle
            servo_controller.set_servo_angle(servo_id = 'servo_1', degree = float(degree))
        elif servo == 'servo_2':
            degree = angle
            servo_controller.set_servo_angle(servo_id = 'servo_2', degree = float(degree))
        elif servo == 'servo_3':
            degree = angle
            servo_controller.set_servo_angle(servo_id = 'servo_3', degree = float(degree))
        elif servo == 'servo_4':
            degree = angle
            servo_controller.set_servo_angle(servo_id = 'servo_4', degree = float(degree))
        elif servo == 'servo_5':
            degree = angle
            servo_controller.set_servo_angle(servo_id = 'servo_5', degree = float(degree))
        elif servo == 'servo_6':
            degree = angle
            servo_controller.set_servo_angle(servo_id = 'servo_6', degree = float(degree))
    
    servo_dict = servo_controller.get_servo_degrees()
    return_value={
        'name': 'dut_server',
        'set_servo': 'successfully',
        'servo_dict': servo_dict,
        'detect': 'None',
#         'temperature': sht40_temp_rh['temperature'],
        'temperature': 'None',
#         'humidity': sht40_temp_rh['relative_humidity'],
        'humidity': 'None',
        'ip_address': IP_address
        }
    
    print(return_value)
    return json.dumps(return_value)

@server.route("/get_info", methods=["GET"])
def get_info(request):
    servo_dict = servo_controller.get_servo_degrees()
    return_value = {
        'name': 'dut_server',
        'get_info': 'successfully',
        'servo_dict': servo_dict,
#         'temperature': sht40_temp_rh['temperature'],
        'temperature': 'None',
#         'humidity': sht40_temp_rh['relative_humidity'],
        'humidity': 'None',
        'ip_address': IP_address
    }
    return json.dumps(return_value)




async def phew_server():
    server.run()

async def device_keep_alive():
    global config
    url_keep = f"http://{config['master_server_ip']}:{config['port']}/server_keep_alive"
    IP_address = check_wifi_status(wifi_manager.wlan, wifi_manager.led)
    servo_dict = servo_controller.get_servo_degrees()
    return_value = {
        'servo_dict': servo_dict,
        'temperature': 'None',
        'humidity': 'None',
        'ip_address': IP_address
    }
    
    return_value = {'name': 'dut_server', 'device_keep_alive': 'successfully','value': return_value}
    payload = return_value
    headers = {'Content-Type': 'application/json', 'Authorization': 'None'}

    response = requests.post(url_keep, json=payload, headers=headers)
    print("Response:", response.text)


async def main():
    global sht40_temp_rh, IP_address
    # Start Phew server
    asyncio.create_task(phew_server())
    #print('--------------------')
    
    while True:
#         sht40_temp_rh = sht40.get_sht40_temp_rh()
        IP_address = check_wifi_status(wifi_manager.wlan, wifi_manager.led)
        
        # Display info on OLED
        oled.info_display(
#             temperatrue=sht40_temp_rh['temperature'],
            temperatrue='None',
#             humidity=sht40_temp_rh['relative_humidity'],
            humidity='None',
            IP_address=IP_address,
            motor_status=servo_controller.get_servo_degrees()
        )
        await device_keep_alive()
        await asyncio.sleep(5)

try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()
