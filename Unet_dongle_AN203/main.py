import machine
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


def send_to_arduino(message):
    uart.write(message)
    print(f"已傳送：{message}")

def receive_from_arduino():
    if uart.any():
        received_message = uart.readline()
        print(f"接收到ASCII：{received_message}")
        hex_representation = ubinascii.hexlify(received_message).decode()
        print(f"接收到ASCII轉16進制：{hex_representation}")
        cleaned_data = [hex_representation[i:i+2] for i in range(0, len(hex_representation), 2)]
        print("return data:", cleaned_data)
        return cleaned_data
    return None

def MC026_UART_RX(cmd):
    header = 'a2ca'
    cmd = cmd.replace(',', '')
    length = '{:02x}'.format(len(cmd) // 2 + 1)
    cal = cmd + length
    split_cal = [cal[i:i+2] for i in range(0, len(cal), 2)]
    sum_cal = 0
    for i in range(len(split_cal)):
        sum_cal = sum_cal + int(split_cal[i], 16)
    cs_decimal = int('a5', 16) - sum_cal
    if cs_decimal > 0:
        cs = '{:02x}'.format(abs(cs_decimal))
    elif cs_decimal < 0:
        if abs(cs_decimal) < 256:
            cs = '{:02x}'.format(int('100', 16) - abs(cs_decimal))
        else:
            while abs(cs_decimal) > 256:
                cs_decimal = abs(int('100', 16) - abs(cs_decimal))
            cs = '{:02x}'.format(int('100', 16) - abs(cs_decimal))
            
    cmd_ready_to_send = header + length + cmd + cs
    print('cs', cs)
    byte_message = bytes.fromhex(cmd_ready_to_send)
    uart.write(byte_message)
    print(f"已傳送：{byte_message}")


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




# WiFi setup
# wifi_manager = WiFiManager(ssid='frank0820_2.4G', password='jotao1218')
wifi_manager = WiFiManager(ssid='dlink-Sales', password='1234567890')
asyncio.run(wifi_manager.connect_to_wifi())
check_interval_sec = 0.25



url = "http://192.168.0.178:5000/receive_ip"
count = 0
while True:
    try:
        
        init_IP_address = check_wifi_status(wifi_manager.wlan, wifi_manager.led)
        payload = {'ip': init_IP_address}
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer your_access_token_here'}

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

        time.sleep(1)

    except OSError as e:
        print(f"OS error occurred: {e}")
        print("Retrying...")
        time.sleep(1)
        
        oled.oled.fill(0)
        oled.oled.text(f'{init_IP_address}', 0, 0)
        oled.oled.text(f'retry:{count}', 0, 30)
        oled.oled.show()
        count = count + 1
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        break  # Exit the loop on unexpected errors



# Define API route for setting servo angles
@server.route("/set_MC026_binding", methods=["GET"])
def set_MC026_binding(request):
    data_in = []
    command = []
    params = request.query_string
    print(params)
    MC026_UART_RX('00,00,03')
    time.sleep(5)
    MC026_UART_RX('00,00,01,00,00')
    
    return_value = {'learning': 'successfully'}
            
    return json.dumps(return_value)

@server.route("/AN203_ON_OFF_test", methods=["GET"])
def AN203_ON_OFF_test(request):
    params = request.query_string
    print(params)
    AN203_ID = '02'
    MC026_UART_RX(f'00,00,02,00,{AN203_ID},01,00,00,00,00,02,01,4e,20')
    time.sleep(5)
    MC026_UART_RX(f'00,00,02,00,{AN203_ID},02,00,00,00,00,02,01,4e,20')
    return_value={'AN203_ON_OFF test': "successfully"}
            
    return json.dumps(return_value)

@server.route("/AN203_ON", methods=["GET"])
def AN203_ON(request):
    params = request.query_string
    print(params)
    AN203_ID = '02'
    MC026_UART_RX(f'00,00,02,00,{AN203_ID},01,00,00,00,00,02,01,4e,20')
    return_value={'AN203_ON': "successfully"}
            
    return json.dumps(return_value)

@server.route("/AN203_OFF", methods=["GET"])
def AN203_OFF(request):
    params = request.query_string
    print(params)
    AN203_ID = '02'
    MC026_UART_RX(f'00,00,02,00,{AN203_ID},02,00,00,00,00,02,01,4e,20')
    return_value={'AN203_OFF': "successfully"}
            
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


