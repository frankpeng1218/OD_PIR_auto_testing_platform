#OD_photo_V1_2_0912
from machine import Pin
import time


gpio_0 = Pin(0, Pin.IN, Pin.PULL_DOWN)
gpio_1 = Pin(1, Pin.IN, Pin.PULL_DOWN)
gpio_2 = Pin(2, Pin.IN, Pin.PULL_DOWN)
gpio_3 = Pin(3, Pin.IN, Pin.PULL_DOWN)
gpio_4 = Pin(4, Pin.IN, Pin.PULL_DOWN)
gpio_5 = Pin(5, Pin.OUT)
gpio_6 = Pin(6, Pin.OUT)
gpio_18 = Pin(18, Pin.IN, Pin.PULL_UP)
gpio_19 = Pin(19, Pin.IN, Pin.PULL_UP)

gpio_7 = Pin(7, Pin.OUT)
gpio_8 = Pin(8, Pin.OUT)
gpio_9 = Pin(9, Pin.OUT)
gpio_13 = Pin(13, Pin.IN, Pin.PULL_UP)
gpio_14 = Pin(14, Pin.IN, Pin.PULL_UP)
gpio_15 = Pin(15, Pin.IN, Pin.PULL_UP)
gpio_16 = Pin(16, Pin.IN, Pin.PULL_DOWN)

led = Pin(25, Pin.OUT)

def initialize():
    gpio_7.value(0)
    gpio_8.value(1)
    gpio_9.value(0)
    led.on()
    print("Initialization: GPIO 7,8,9 = [0,1,0], LED ON")
    time.sleep(0.5)

    gpio_7.value(0)
    gpio_8.value(0)
    gpio_9.value(0)
    led.off()
    print("Initialization completed: GPIO 7,8,9 = [0,0,0], LED OFF")

def debounce(pin):
    time.sleep(0.01)
    return pin.value() == 0

def check_gpio_01234():
    gpio_states = [
        gpio_0.value(),
        gpio_1.value(),
        gpio_2.value(),
        gpio_3.value(),
        gpio_4.value()
    ]
    
    print(f"GPIO 0,1,2,3,4 = {gpio_states}")



initialize()

previous_gpio_16_value = 0
last_gpio_check_time = time.time()

while True:
    current_gpio_16_value = gpio_16.value()

    if time.time() - last_gpio_check_time >= 2:
        check_gpio_01234()
        last_gpio_check_time = time.time()

    if current_gpio_16_value == 1 and previous_gpio_16_value == 0:
        start_time = time.ticks_us()

        gpio_7.value(1)
        gpio_8.value(0)
        gpio_9.value(0)
        print("GPIO 16 is HIGH, GPIO 7,8,9 = [1,0,0]")

        end_time = time.ticks_us()
        time_elapsed = time.ticks_diff(end_time, start_time)
        print(f"Time elapsed from GPIO 16 HIGH to 001 state: {time_elapsed} microseconds")

        for _ in range(3):
            led.on()
            time.sleep(0.1)
            led.off()
            time.sleep(0.1)
        print("LED blinked 3 times")

    previous_gpio_16_value = current_gpio_16_value

    if gpio_13.value() == 0 and debounce(gpio_13):
        gpio_7.value(1)
        gpio_8.value(0)
        gpio_9.value(0)
        print("GPIO 7,8,9 = [1,0,0]")

        led.on()
        time.sleep(0.1)
        led.off()

        while gpio_13.value() == 0:
            time.sleep(0.01)

    elif gpio_14.value() == 0 and debounce(gpio_14):
        gpio_7.value(0)
        gpio_8.value(1)
        gpio_9.value(0)
        print("GPIO 7,8,9 = [0,1,0]")

        led.on()
        time.sleep(0.1)
        led.off()

        time.sleep(0.5)

        gpio_8.value(0)
        print("GPIO 8 恢復為 0")

        while gpio_14.value() == 0:
            time.sleep(0.01)

    elif gpio_15.value() == 0 and debounce(gpio_15):
        gpio_7.value(0)
        gpio_8.value(0)
        gpio_9.value(1)
        print("GPIO 7,8,9 = [0,0,1]")

        led.on()
        time.sleep(0.1)
        led.off()

        while gpio_15.value() == 0:
            time.sleep(0.01)

    if gpio_18.value() == 0:
        print("GPIO 18 is LOW, pulsing GPIO 5")

        gpio_5.on()
        time.sleep(0.3)
        gpio_5.off()

        led.on()
        time.sleep(0.1)
        led.off()

    if gpio_19.value() == 0:
        print("GPIO 19 is LOW, pulsing GPIO 6")

        gpio_6.on()
        time.sleep(0.3)
        gpio_6.off()

        led.on()
        time.sleep(0.1)
        led.off()

    time.sleep(0.01)
