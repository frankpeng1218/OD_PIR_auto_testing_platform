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


gpio_0_led_velocity_25 = Pin(0, Pin.IN, Pin.PULL_DOWN)
gpio_1_led_velocity_50 = Pin(1, Pin.IN, Pin.PULL_DOWN)
gpio_2_led_velocity_75 = Pin(2, Pin.IN, Pin.PULL_DOWN)
gpio_3_led_velocity_100 = Pin(3, Pin.IN, Pin.PULL_DOWN)

gpio_4_led_power = Pin(4, Pin.IN, Pin.PULL_DOWN)

gpio_5_velocity_control = Pin(5, Pin.OUT)
gpio_6_direction_switch = Pin(6, Pin.OUT)
gpio_7_run = Pin(7, Pin.OUT)
gpio_8_release = Pin(8, Pin.OUT)
gpio_9_stop = Pin(9, Pin.OUT)


gpio_16_photo_right = Pin(16, Pin.IN, Pin.PULL_DOWN)
gpio_20_photo_right_stop = Pin(20, Pin.IN, Pin.PULL_DOWN)
gpio_21_photo_wheel = Pin(21, Pin.IN, Pin.PULL_DOWN)
gpio_22_photo_left_stop = Pin(22, Pin.IN, Pin.PULL_DOWN)

led_onboard = Pin("LED", Pin.OUT, value=0)


def hardware_initialize():
    gpio_7_run.value(0)
    gpio_8_release.value(1)
    gpio_9_stop.value(0)
    led_onboard.on()
    print("Initialization: GPIO 7,8,9 = [0,1,0], LED ON")
    time.sleep(0.5)
    
    gpio_7_run.value(0)
    gpio_8_release.value(0)
    gpio_9_stop.value(0)
    led_onboard.off()
    print("Initialization completed: GPIO 7,8,9 = [0,0,0], LED OFF")





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





def sb_status_check():
    with open('sb_status.txt', 'r') as file:
        lines = file.readlines()
    # 確保 lines 的長度是2，分別對應標題行和數據行
    if len(lines) != 2:
        raise ValueError("sb_status.txt 文件格式不正確，需要兩行（標題和數據）。")
    # 提取數據並轉換為字典
    keys = lines[0].strip().split()  # 這應該是 ['track', 'track_number', 'direction']
    values = lines[1].strip().split()  # 這應該是 ['right', '0', 'forward']
    # 確保 keys 和 values 的數量相同
    if len(keys) != len(values):
        raise ValueError("標題和數據的項目數量不匹配。")
    # 將 keys 和 values 組合成字典
    location = dict(zip(keys, values))
    return location


def moving_direction_switch():
    gpio_6_direction_switch.on()
    time.sleep(0.3)
    gpio_6_direction_switch.off()
    
    time.sleep(0.5)
    
    gpio_6_direction_switch.on()
    time.sleep(0.3)
    gpio_6_direction_switch.off()

def moving_one_step(track):
    gpio_7_run.value(1)
    gpio_8_release.value(0)
    gpio_9_stop.value(0)
    led_onboard.value(1)
    time.sleep(0.5)
    led_onboard.value(0)

    # 持續檢查 GPIO 20 的狀態
    if track == 'right':
        while True:
            if gpio_20_photo_right_stop.value() == 1:
                # 一旦 GPIO 20 變成高電平，將 GPIO 7, 8, 9 設置為 [0, 0, 1]
                gpio_7_run.value(0)
                gpio_8_release.value(0)
                gpio_9_stop.value(1)
                led_onboard.value(1)
                time.sleep(0.3)
                led_onboard.value(0)
                break  # 退出迴圈
    elif track == 'left':         
        while True:
            if gpio_22_photo_left_stop.value() == 1:
                # 一旦 GPIO 20 變成高電平，將 GPIO 7, 8, 9 設置為 [0, 0, 1]
                gpio_7_run.value(0)
                gpio_8_release.value(0)
                gpio_9_stop.value(1)
                led_onboard.value(1)
                time.sleep(0.3)
                led_onboard.value(0)
                break  # 退出迴圈
    print('moving OK')
        
def update_sb_status(new_track, new_track_number, new_direction):
    # 讀取文件內容
    with open('sb_status.txt', 'r') as file:
        lines = file.readlines()

    # 確保文件格式符合預期
    if len(lines) != 2:
        raise ValueError("sb_status.txt 文件格式不正確，需要有兩行。")

    # 創建新的第二行內容
    updated_line = f"{new_track} {new_track_number} {new_direction}\n"

    # 將更新後的內容寫回文件
    with open('sb_status.txt', 'w') as file:
        file.write(lines[0])  # 寫入第一行（列名）
        file.write(updated_line)  # 寫入新的數據行

    # 返回更新後的字典
    location = {'track': new_track, 'track_number': new_track_number, 'direction': new_direction}
    
    print('!!!!!!!!!!!',location)
    return location




def sb_moving(track, track_number, direction):
    location = sb_status_check()
    past_track = location['track']
    past_track_number = location['track_number']
    past_track_direction = location['direction']
    demand_track = track
    demand_track_number = track_number
    demand_direction = direction
    # 排除切換track的動作
    # 比較上一個track和目標track
    print('demand_track:',demand_track)
    print('demand_track_number:',demand_track_number)
    print('demand_direction:',demand_direction)
    print('past_track_number:',past_track_number)
    print('demand_track_number:',demand_track_number)
    if demand_direction == 'backforward' and int(past_track_number)<int(demand_track_number):
        return 'backforward value invalid'
    elif demand_direction == 'forward' and int(past_track_number)>int(demand_track_number):
        return 'backforward value invalid'
    
    if demand_track == past_track:
        if demand_direction == past_track_direction and demand_direction == 'forward':
            for i in range(abs((int(demand_track_number)-int(past_track_number)))):
                moving_one_step(demand_track)
                time.sleep(3)
            return update_sb_status(demand_track, demand_track_number, demand_direction)         
        elif demand_direction == past_track_direction and demand_direction == 'backforward':
            for i in range(abs((int(demand_track_number)-int(past_track_number)))):
                moving_one_step(demand_track)
                time.sleep(3)
            return update_sb_status(demand_track, demand_track_number, demand_direction)
                
        elif demand_direction != past_track_direction and demand_direction == 'forward':
            moving_direction_switch()
            for i in range(abs((int(demand_track_number)-int(past_track_number)))):
                moving_one_step(demand_track)
                time.sleep(3)
            return update_sb_status(demand_track, demand_track_number, demand_direction)
        elif demand_direction != past_track_direction and demand_direction == 'backforward':               
            moving_direction_switch()
            for i in range(abs((int(demand_track_number)-int(past_track_number)))):
                moving_one_step(demand_track)
                time.sleep(3)
            return update_sb_status(demand_track, demand_track_number, demand_direction)
    # 轉換track            
    elif demand_track != past_track:
        if past_track_number != '0':
            return 'You must keep the same track and move the track_number to 0 for switching the track'
        
        elif past_track_number == '0':
            update_sb_status(demand_track, track_number, direction)
            print('switch track OK')
            return sb_moving(demand_track, track_number, direction)
    else:
        return sb_status_check()

with open('configuration.txt', 'r') as file:
    lines = file.readlines()
header = lines[0].strip().split() 
data = lines[1].strip().split()    
config = dict(zip(header, data))

# WiFi setup
wifi_manager = WiFiManager(ssid=config['ssid'], password=config['password'])
#wifi_manager = WiFiManager(ssid='dlink-Sales', password='1234567890')
asyncio.run(wifi_manager.connect_to_wifi())
check_interval_sec = 0.25


url = f"http://{config['master_server_ip']}:{config['port']}/receive_ip"
count = 0

while True:
    try:
        
        sb_server_ip = check_wifi_status(wifi_manager.wlan, wifi_manager.led)
        payload = {'name': 'sb_server','ip_address': sb_server_ip}
        headers = {'Content-Type': 'application/json', 'Authorization': 'None'}

        
        oled.oled.fill(0)
        oled.oled.text(f'{sb_server_ip}', 0, 0)
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
        oled.oled.text(f'{sb_server_ip}', 0, 0)
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
        oled.oled.text(f'{sb_server_ip}', 0, 0)
        oled.oled.text(f'Connecting to', 0, 15)
        oled.oled.text(f'master server', 0, 25)
        oled.oled.text(f'{config['master_server_ip']}', 0, 35)
        oled.oled.text(f':{config['port']}', 0, 45)
        oled.oled.text(f'retry:{count}', 0, 55)
        oled.oled.show()
        count = count + 1
        break  # Exit the loop on unexpected errors

oled.oled.fill(0)
oled.oled.text(f"{sb_server_ip}", 0, 0)
oled.oled.text(f"initialization", 0, 20)
oled.oled.show()
    
hardware_initialize()

oled.oled.fill(0)
oled.oled.text(f'sb_server:', 0, 0)
oled.oled.text(f'{sb_server_ip}', 0, 10)
oled.oled.text(f'Waiting for cmd', 0, 20)
oled.oled.show()




# Define API route for setting servo angles
@server.route("/move", methods=["POST"])
def move(request):
    global oled
    
    params = request.query_string
    print('params:', params)
    
    sb_dict = {}
    if params:
        pairs = params.split('&')
        for pair in pairs:
            key, value = pair.split('=')
            sb_dict[key] = value

    # 擷取參數值
    track = sb_dict.get('track')
    track_number = sb_dict.get('track_number')
    direction = sb_dict.get('direction')
    
    
    location = sb_moving(track, track_number, direction)
    if type(location) is not str:
        print('llllllll',location)
        oled.oled.fill(0)
        oled.oled.text(f"{sb_server_ip} ", 0, 0)
        oled.oled.text(f"track:{location['track']}", 0, 20)
        oled.oled.text(f"track_number:{location['track_number']}", 0, 30)
        oled.oled.text(f"direction:{location['direction']}", 0, 40)
        oled.oled.show()
            
        return_value = {'name': 'sb_server', 'move': 'successfully', 'location': location}
    else:
        return_value = location
        
    return json.dumps(return_value)

@server.route("/get_info", methods=["GET"])
def get_info(request):
    location = sb_status_check()
    return_value = {'name': 'sb_server', 'get_info': 'successfully','location': location}
    return json.dumps(return_value)



async def phew_server():
    server.run()

async def device_keep_alive():
    global config
    url_keep = f"http://{config['master_server_ip']}:{config['port']}/server_keep_alive"
    
    return_value = {'name': 'sb_server', 'device_keep_alive': 'successfully','location': sb_status_check(), 'ip_address': sb_server_ip}
    payload = return_value
    headers = {'Content-Type': 'application/json', 'Authorization': 'None'}

    response = requests.post(url_keep, json=payload, headers=headers)
    print("Response:", response.text)

async def main():
    # Start Phew server
    asyncio.create_task(phew_server())

    while True:
        IP_address = check_wifi_status(wifi_manager.wlan, wifi_manager.led)
        print("IP_address:",IP_address)
        current_location = sb_status_check()
        # Display info on OLED
        oled.oled.fill(0)
        oled.oled.text(f"{IP_address} ", 0, 0)
        oled.oled.text(f"track:{current_location['track']}", 0, 20)
        oled.oled.text(f"track_number:{current_location['track_number']}", 0, 30)
        oled.oled.text(f"direction:{current_location['direction']}", 0, 40)
        oled.oled.show()
        # Run device_keep_alive() every 5 seconds
        await device_keep_alive()
        await asyncio.sleep(5)# 改這邊控制秒數

try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()



