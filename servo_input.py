import time
import network
import uasyncio as asyncio
from machine import Pin
from servo import Servo

#----------------------------general----------------------------
led = Pin("LED", Pin.OUT, value=1)
#----------------------------general----------------------------

#----------------------------servo motor----------------------------
my_servo = Servo(pin_id=0)
global servo_degree
servo_degree = 0
my_servo.write(servo_degree)
#----------------------------servo motor----------------------------

#--------------Configure your WiFi SSID and password--------------
ssid = 'dlink-Sales'
password = '1234567890'
check_interval_sec = 0.25
wlan = network.WLAN(network.STA_IF)
#--------------Configure your WiFi SSID and password--------------

#-------------------HTML-------------------------
html = """<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="data:,">
<style>
html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center; }
.button { background-color: #4CAF50; border: 2px solid #000000; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; }
.textbox { width: 100px; padding: 10px; font-size: 16px; }
</style>
</head>
<body>
<center>
<h1>Servo Control</h1>
<form>
  <label for="angle">Enter Servo Angle (0-180):</label>
  <input type="number" id="angle" name="angle" min="0" max="180" class="textbox">
  <button class="button" name="submit_angle" value="submit" type="submit">Set Angle</button>
</form>
<p>%s</p>
</center>
</body>
</html>
"""
#-------------------HTML-------------------------

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
def servo_move(degree):
    my_servo.write(degree)
#------------------------------servo motor def------------------------------

async def connect_to_wifi():
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
        time.sleep(1)

    # Handle connection error
    if wlan.status() != 3:
        blink_led(0.1, 10)
        raise RuntimeError('WiFi connection failed')
    else:
        blink_led(0.5, 2)
        print('connected')
        status = wlan.ifconfig()
        print('ip = ' + status[0])


async def serve_client(reader, writer):
    global servo_degree
    print("Client connected")
    request_line = await reader.readline()
    print("Request:", request_line)
    # We are not interested in HTTP request headers, skip them
    while await reader.readline() != b"\r\n":
        pass
    
    # find valid commands within the request
    request = str(request_line)
    angle_index = request.find('angle=')
    
    # Check if angle value is present in the request
    if angle_index != -1:
        # Extract the angle value from the request
        angle_str = request[angle_index:].split('&')[0].split('=')[1]
        try:
            angle = int(angle_str)
            if 0 <= angle <= 180:
                servo_degree = angle
                servo_move(servo_degree)
                stateis = f"Set servo angle to {angle} degrees"
                print(stateis)
        except ValueError:
            stateis = "Invalid angle value"
            print(stateis)
    
    else:
        stateis = "No valid command found"
        print(stateis)
    
    # response = html % stateis
    response = stateis
    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    writer.write(response)

    await writer.drain()
    await writer.wait_closed()

async def main():
    print('Connecting to WiFi...')
    asyncio.create_task(connect_to_wifi())

    print('Setting up webserver...')
    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))
    while True:
        await asyncio.sleep(check_interval_sec)

try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()
