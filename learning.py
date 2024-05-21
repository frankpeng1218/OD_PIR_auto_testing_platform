

import time
from machine import Pin, I2C
from micropython_sht4x import sht4x
from ssd1306 import SSD1306_I2C
import network
import uasyncio as asyncio



def read_html_file(filename):
    with open(filename, 'r') as file:
        return file.read()


html_template = read_html_file('index.html')

#--------------Configure your WiFi SSID and password--------------
ssid = 'dlink-Sales'
password = '1234567890'
check_interval_sec = 0.25
wlan = network.WLAN(network.STA_IF)
#--------------Configure your WiFi SSID and password--------------


led = Pin("LED", Pin.OUT, value=1)



i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)  # RP2040 的正確 I2C pin


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
#------------------------------general def------------------------------
def toggle_led(led):
    led.toggle()

def blink_led(frequency=0.5, num_blinks=3):
    for _ in range(num_blinks):
        led.on()
        time.sleep(frequency)
        led.off()
        time.sleep(frequency)

async def connect_to_wifi():
    global ip_address
    wlan.active(True)
    wlan.config(pm=0xa11140) 
    wlan.connect(ssid, password)

    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)


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

        while await reader.readline() != b"\r\n":
            pass
        

        request = str(request_line)

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
    print('Connecting to WiFi...')
    await connect_to_wifi()
    print(f'Stored IP Address: {ip_address}')
    
    print('Setting up webserver...')
    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))
    while True:
        temp_and_humid_read_and_display()
        await asyncio.sleep(check_interval_sec)


try:
    asyncio.run(main())  
finally:
    asyncio.new_event_loop()
