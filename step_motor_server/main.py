from lib_frank.servo_controller import ServoController
from lib_frank.oled_display import Oled_Display
from lib_frank.sht40_detect import sht40_Detect
from lib_frank.wifi_connect import WiFiManager
import time
import uasyncio as asyncio
from phew import server
import json
import urequests as requests

global servo_controller

# Initialize components
servo_controller = ServoController()
oled = Oled_Display()
sht40 = sht40_Detect()

# WiFi setup
wifi_manager = WiFiManager(ssid='frank0820_2.4G', password='jotao1218')
asyncio.run(wifi_manager.connect_to_wifi())

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

url = "http://192.168.15.109:5000/receive_ip"

while True:
    try:
        init_IP_address = check_wifi_status(wifi_manager.wlan, wifi_manager.led)
        payload = {'ip': init_IP_address}

        response = requests.post(url, json=payload)
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

        time.sleep(1)

    except OSError as e:
        print(f"OS error occurred: {e}")
        print("Retrying...")
        time.sleep(1)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        break  # Exit the loop on unexpected errors



check_interval_sec = 0.25


# Define API route for setting servo angles
@server.route("/set_servo", methods=["GET","POST"])
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
    
    
    return_value={
        'communication': 'good',
        'servo_dict': servo_dict,
        'detect': 'yes',
        'temperature': sht40_temp_rh['temperature'],
        'humidity': sht40_temp_rh['relative_humidity'],
        'ip_address': IP_address
        }
    
    print(return_value)
 #   response = {
 #       'status': 'success',
 #       'angles': angle_values,
 #       'temperature': sht40_temp_rh['temperature'],
 #       'humidity': sht40_temp_rh['relative_humidity'],
#        'IP_address': IP_address,
#        'motor_status': servo_controller.get_servo_degrees()
#    }
    return json.dumps(return_value)

async def phew_server():
    server.run()
    
async def main():
    global sht40_temp_rh, IP_address
    # Start Phew server
    asyncio.create_task(phew_server())
    #print('--------------------')
    
    while True:
        sht40_temp_rh = sht40.get_sht40_temp_rh()
        IP_address = check_wifi_status(wifi_manager.wlan, wifi_manager.led)
        
        # Display info on OLED
        oled.info_display(
            temperatrue=sht40_temp_rh['temperature'],
            humidity=sht40_temp_rh['relative_humidity'],
            IP_address=IP_address,
            motor_status=servo_controller.get_servo_degrees()
        )
        await asyncio.sleep(check_interval_sec)

try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()
