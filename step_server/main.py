import machine
from machine import Pin, PWM
import time
import ubinascii

from lib_frank.wifi_connect import WiFiManager
from lib_frank.oled_display import Oled_Display

import urequests as requests
import time
import uasyncio as asyncio
from phew import server
import json
# Initialize UART
uart = machine.UART(0, baudrate=19200, tx=machine.Pin(0), rx=machine.Pin(1))
oled = Oled_Display()

# Check WiFi status
def check_wifi_status(wlan, led):
    if wlan.isconnected():
        ip_address = wlan.ifconfig()[0]
    else:
        print('WIFI 断线')
        led.off()
        asyncio.run(wifi_manager.connect_to_wifi())
    time.sleep(1)
    return ip_address


# 初始化引腳
step_pin_2 = Pin(2, Pin.OUT)
dir_pin_3 = Pin(3, Pin.OUT)
en_pin_4 = Pin(4, Pin.OUT)
alarm_pin_5 = Pin(5, Pin.IN)

step_pin_2.value(0)
dir_pin_3.value(0)# 1 為順時針，0 為逆時針
en_pin_4.value(1)


# 定義步進函數
def step_controller(steps, delay):
    for _ in range(steps):
        step_pin_2.value(1)
        time.sleep(delay)
        step_pin_2.value(0)
        time.sleep(delay)

# 步進馬達config，PULSE/REV:2000，2000個pulse等於轉一圈
steps_per_revolution = 1
step_delay = 0.001  # 0.5s 延遲
wheel_radius = 0.5 #0.5m
distance_per_pulse = (2 * 3.14159265 * wheel_radius)/2000


# 假設這些是你的步進馬達控制函數和設定
def step_controller(steps, delay):
    for _ in range(steps):
        step_pin_2.value(1)
        time.sleep(delay)
        step_pin_2.value(0)
        time.sleep(delay)

# 計算每個pulse對應的距離
distance_per_pulse = (2 * 3.14159265 * wheel_radius) / 2000

def move_distance(desired_distance):
    # 計算需要的pulse數
    desired_pulse_count = round(desired_distance / distance_per_pulse)
    # 調用步進馬達控制函數，使其移動到目標位置
    step_controller(desired_pulse_count, step_delay)
    return str(desired_pulse_count*distance_per_pulse)



with open('configuration.txt', 'r') as file:
    lines = file.readlines()
header = lines[0].strip().split() 
data = lines[1].strip().split()    
config = dict(zip(header, data))

# WiFi setup
wifi_manager = WiFiManager(ssid=config['ssid'], password=config['password'])
# wifi_manager = WiFiManager(ssid='dlink-Sales', password='1234567890')
asyncio.run(wifi_manager.connect_to_wifi())
check_interval_sec = 0.25


url = f"http://{config['master_server_ip']}:{config['port']}/receive_ip"
count = 0


while True:
    try:
        
        step_server_ip = check_wifi_status(wifi_manager.wlan, wifi_manager.led)
        payload = {'name': 'step_server','ip_address': step_server_ip}
        headers = {'Content-Type': 'application/json', 'Authorization': 'None'}

        
        oled.oled.fill(0)
        oled.oled.text(f'{step_server_ip}', 0, 0)
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
        oled.oled.text(f'{step_server_ip}', 0, 0)
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
        oled.oled.text(f'{step_server_ip}', 0, 0)
        oled.oled.text(f'Connecting to', 0, 15)
        oled.oled.text(f'master server', 0, 25)
        oled.oled.text(f'{config['master_server_ip']}', 0, 35)
        oled.oled.text(f':{config['port']}', 0, 45)
        oled.oled.text(f'retry:{count}', 0, 55)
        oled.oled.show()
        count = count + 1
        break  # Exit the loop on unexpected errors

oled.oled.fill(0)
oled.oled.text(f"{step_server_ip}", 0, 0)
oled.oled.text(f"initialization", 0, 20)
oled.oled.show()
    
    
    
with open('step_past_position.txt', 'r') as file:
    # 讀取檔案內容
    content = file.read()
    # 將內容轉換為浮點數或者需要的格式
    past_position = float(content)  # 假設讀取的是浮點數值
    
dir_pin_3.value(0)
init_zero_position = move_distance(float(past_position+0.05))
real_position = 0
with open('step_past_position.txt', 'w') as file:
    file.write(str(real_position))
    
    

oled.oled.fill(0)
oled.oled.text(f'step_server:', 0, 0)
oled.oled.text(f'{step_server_ip}', 0, 10)
oled.oled.text(f'Waiting for cmd', 0, 20)
oled.oled.show()




# Define API route for setting servo angles
@server.route("/set_distance", methods=["POST"])
def set_distance(request):
    global oled
    
    params = request.query_string
    print('params:',params)
    pairs = params.split('&')
    step_dict = {}
    for pair in pairs:
        key, value = pair.split('=')
        step_dict[key] = value
    print('-------')
    print('step_dict:',step_dict)
    
    wanted_position = float(step_dict['position'])
    
    with open('step_past_position.txt', 'r') as file:
        content = file.read()
        past_position = float(content)
    if past_position <= wanted_position:
        dir_pin_3.value(1)
        run_position = wanted_position-past_position
        run_position = move_distance(run_position)
        real_position = str(past_position + float(run_position))
    else:
        dir_pin_3.value(0)
        run_position = abs(wanted_position-past_position)
        run_position = move_distance(run_position)
        real_position = str(past_position - float(run_position))   

    oled.oled.fill(0)
    oled.oled.text(f"{step_server_ip} ", 0, 0)
    oled.oled.text(f"position from 0:", 0, 20)
    oled.oled.text(f"{real_position}", 0, 30)
    oled.oled.show()
        
    with open('step_past_position.txt', 'w') as file:
        file.write(real_position)
    
    
    return_value = {'name': 'step_server', 'set_distance': 'successfully', 'real_position': real_position}
            
    return json.dumps(return_value)

@server.route("/get_info", methods=["GET"])
def get_info(request):
    
    with open('step_past_position.txt', 'r') as file:
        content = file.read()
        
    return_value = {'name': 'step_server', 'get_info': 'successfully','real_position': content}
    return json.dumps(return_value)

async def phew_server():
    server.run()

async def main():
    # Start Phew server
    asyncio.create_task(phew_server())

    while True:
        IP_address = check_wifi_status(wifi_manager.wlan, wifi_manager.led)
#         print("IP_address:",IP_address)
        # Display info on OLED
        await asyncio.sleep(check_interval_sec)

try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()

