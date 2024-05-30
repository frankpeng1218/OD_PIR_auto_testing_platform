import time
import network
import uasyncio as asyncio
from machine import Pin

class WiFiManager:
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
        self.wlan = network.WLAN(network.STA_IF)
        self.led = Pin("LED", Pin.OUT, value=1)  # 假设Pin "LED" 对你的板子是正确的

    def blink_led(self, frequency=0.5, num_blinks=3):
        """以给定频率闪烁LED，闪烁指定次数。"""
        for _ in range(num_blinks):
            self.led.on()
            time.sleep(frequency)
            self.led.off()
            time.sleep(frequency)

    async def connect_to_wifi(self):
        """尝试连接WiFi，在连接尝试期间闪烁LED。"""
        self.wlan.active(True)
        self.wlan.config(pm=0xa11140)  # 禁用省电模式

        while not self.wlan.isconnected():
            print("尝试连接WiFi...")
            self.wlan.connect(self.ssid, self.password)

            # 等待连接建立
            max_wait = 10
            while max_wait > 0:
                if self.wlan.status() < 0 or self.wlan.status() >= 3:
                    break
                max_wait -= 1
                self.blink_led(0.1, 1)  # 连接尝试期间闪烁LED
                await asyncio.sleep(1)

            # 检查连接状态
            if self.wlan.status() == 3:
                ip_address = self.wlan.ifconfig()[0]
                print('已连接，IP地址:', ip_address)
                self.led.on()  # 连接成功时点亮LED
                return
            else:
                print('连接失败，重试中...')
                self.blink_led(0.1, 10)  # 失败时快速闪烁
                await asyncio.sleep(1)  # 重试前等待一段时间



