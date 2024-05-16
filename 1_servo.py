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
<script>
function updateValue(inputId) {
    var input = document.getElementById(inputId);
    localStorage.setItem(inputId, input.value);
}
function loadValues() {
    var inputIds = ['angle1', 'angle2', 'angle3', 'angle4', 'angle5', 'angle6'];
    inputIds.forEach(function(inputId) {
        var input = document.getElementById(inputId);
        var savedValue = localStorage.getItem(inputId);
        if (savedValue) {
            input.value = savedValue;
        }
    });
}
</script>
</head>
<body onload="loadValues()">
<center>
<h1>Servo Control</h1>
<form>
  <label for="angle1">Enter Servo 1 Angle (0-180):</label>
  <input type="number" id="angle1" name="angle1" min="0" max="180" class="textbox" oninput="updateValue('angle1')"><br>
  
  <label for="angle2">Enter Servo 2 Angle (0-180):</label>
  <input type="number" id="angle2" name="angle2" min="0" max="180" class="textbox" oninput="updateValue('angle2')"><br>
  
  <label for="angle3">Enter Servo 3 Angle (0-180):</label>
  <input type="number" id="angle3" name="angle3" min="0" max="180" class="textbox" oninput="updateValue('angle3')"><br>
  
  <label for="angle4">Enter Servo 4 Angle (0-180):</label>
  <input type="number" id="angle4" name="angle4" min="0" max="180" class="textbox" oninput="updateValue('angle4')"><br>
  
  <label for="angle5">Enter Servo 5 Angle (0-180):</label>
  <input type="number" id="angle5" name="angle5" min="0" max="180" class="textbox" oninput="updateValue('angle5')"><br>
  
  <label for="angle6">Enter Servo 6 Angle (0-180):</label>
  <input type="number" id="angle6" name="angle6" min="0" max="180" class="textbox" oninput="updateValue('angle6')"><br>
  
  <button class="button" name="submit_angle" value="submit" type="submit">Set Angles</button>
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
    global servo_degree_1, servo_degree_2, servo_degree_3, servo_degree_4, servo_degree_5, servo_degree_6
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
    response = html % stateis
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


