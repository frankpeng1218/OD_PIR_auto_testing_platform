from machine import Pin, PWM
import time



# 初始化引腳
step_pin_2 = Pin(2, Pin.OUT)
dir_pin_3 = Pin(3, Pin.OUT)
en_pin_4 = Pin(4, Pin.OUT)
alarm_pin_5 = Pin(5, Pin.IN)

step_pin_2.value(0)
dir_pin_3.value(0)# 1 為順時針，0 為逆時針
en_pin_4.value(1)


# 定義步進函數
def step(steps, delay):
    for _ in range(steps):
        step_pin_2.value(1)
        time.sleep(delay)
        step_pin_2.value(0)
        time.sleep(delay)

# 步進馬達config，PULSE/REV:2000，2000個pulse等於轉一圈
steps_per_revolution = 1
step_delay = 0.001  # 0.5s 延遲
wheel_radius = 0.5 #0.5m
distance_per_pulse = (2 * 3.14159265 * 0.5)/2000


step(steps_per_revolution, step_delay)


# Define API route for setting servo angles
@server.route("/set_distance", methods=["POST"])
def set_distance(request):
    global oled
    oled.oled.fill(0)
    oled.oled.text(f'unet_server:', 0, 0)
    oled.oled.text(f'{unet_server_ip}', 0, 10)
    oled.oled.text(f'set_MC026_binding', 0, 20)
    oled.oled.show()
    
    data_in = []
    command = []
    params = request.query_string
    print(params)
    
    MC026_UART_RX('00,00,03')
    time.sleep(5)
    MC026_UART_RX('00,00,01,00,00')
    
    return_value = {'set_distance': 'successfully'}
            
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

