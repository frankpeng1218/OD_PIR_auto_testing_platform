import time
import ntptime
from machine import Pin, I2C
from micropython_sht4x import sht4x
from ssd1306 import SSD1306_I2C

import network
import uasyncio as asyncio
from servo import Servo
import utime

#-------------------HTML-------------------------

# Function to read HTML file content
def read_html_file(filename):
    with open(filename, 'r') as file:
        return file.read()

# Load the HTML content from the file
html_template = read_html_file('index.html')
#-------------------HTML-------------------------

#--------------Configure your WiFi SSID and password--------------
ssid = 'dlink-Sales'
#ssid = 'dlink'
password = '1234567890'
check_interval_sec = 0.25
wlan = network.WLAN(network.STA_IF)
#--------------Configure your WiFi SSID and password--------------


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
# 定義 I2C pin
i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)  # RP2040 的正確 I2C pin

# 初始化 SHT4X 感測器和 SSD1306 顯示器
sht = sht4x.SHT4X(i2c=i2c, address=0x44)
oled = SSD1306_I2C(width=128, height=64, i2c=i2c, addr=0x3C)

ip_address = "Not Connected" 

def temp_and_humid_read_and_display():
    global ip_address
    """
    讀取溫度和相對濕度並顯示在 OLED 顯示器上。
    """
    temperature, relative_humidity = sht.measurements
    
    oled.fill(0)
    oled.text(f"Temp :{temperature:.2f} C", 0, 0)
    oled.text(f"Humid:{relative_humidity:.2f} %", 0, 10)
    oled.text(f"IP:{ip_address} ", 0, 20)
    oled.show()

# Initialize NTP time



def get_network_time():
    try:
        # Synchronize time with NTP server
        ntptime.settime()
        # Return the current time in local time format
        current_time = utime.localtime()
        print('Current time:', current_time)
        return current_time
    except Exception as e:
        print("Failed to get network time:", e)
        # Return a default time if network time sync fails
        return (2021, 1, 1, 0, 0, 0, 0, 0)

def log_data_to_file():
    global ip_address
    temperature, relative_humidity = sht.measurements
    current_time = get_network_time()
    timestamp = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        current_time[0], current_time[1], current_time[2],
        current_time[3], current_time[4], current_time[5]
    )
    with open('data_log.txt', 'a') as file:
        file.write(f"{timestamp} - Temp: {temperature:.2f} C, Humid: {relative_humidity:.2f} %, IP: {ip_address}\n")
    print('Time recorded')
    
async def log_data_periodically(interval_minutes):
    while True:
        log_data_to_file()
        await asyncio.sleep(interval_minutes * 60)
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

async def connect_to_wifi():
    global ip_address
    wlan.active(True)
    wlan.config(pm=0xa11140)  # Disable powersave mode
    wlan.connect(ssid, password)

    # Wait for connect or fail
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        await asyncio.sleep(1)  # 使用 uasyncio.sleep 而不是 time.sleep

    # Handle connection error
    if wlan.status() != 3:
        blink_led(0.1, 10)
        raise RuntimeError('WiFi connection failed')
    else:
        blink_led(0.5, 2)
        print('connected')
        status = wlan.ifconfig()
        ip_address = status[0]

async def serve_client(reader, writer):
    global servo_degree_1, servo_degree_2, servo_degree_3, servo_degree_4, servo_degree_5, servo_degree_6
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
                servo_degree_1 = angle
                servo_move_1(servo_degree_1)
            elif servo == 'servo_2':
                servo_degree_2 = angle
                servo_move_2(servo_degree_2)
            elif servo == 'servo_3':
                servo_degree_3 = angle
                servo_move_3(servo_degree_3)
            elif servo == 'servo_4':
                servo_degree_4 = angle
                servo_move_4(servo_degree_4)
            elif servo == 'servo_5':
                servo_degree_5 = angle
                servo_move_5(servo_degree_5)
            elif servo == 'servo_6':
                servo_degree_6 = angle
                servo_move_6(servo_degree_6)
        
        stateis = f"Set servo angles: {angle_values}"
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
    
async def test():
    await asyncio.sleep(0.5)  # Simulate an asynchronous I/O operation
    print("Test completed")

async def main():
    print('Connecting to WiFi...')
    task_wifi_connect = asyncio.create_task(connect_to_wifi())
    
    task_test = asyncio.create_task(test())
    await asyncio.gather(task_wifi_connect, task_test)
    print(f'Stored IP Address: {ip_address}')
    print('Setting up webserver...')
    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))
    asyncio.create_task(log_data_periodically(0.5))  # Run the logging task every 10 minutes
    while True:
        temp_and_humid_read_and_display()
        await asyncio.sleep(check_interval_sec)


try:
    asyncio.run(main())  
finally:
    asyncio.new_event_loop()
