from machine import Pin, PWM
import time

# 設定 GPIO 引腳
STEP_PIN = 2  # 步進訊號引腳
DIR_PIN = 3   # 方向訊號引腳
EN_PIN = 4    # 使能訊號引腳
ALARM_PIN = 5

# 初始化引腳
step_pin = Pin(STEP_PIN, Pin.OUT)
dir_pin = Pin(DIR_PIN, Pin.OUT)
en_pin = Pin(EN_PIN, Pin.OUT)
alarm_pin = Pin(ALARM_PIN, Pin.OUT)
# 使能步進馬達
alarm_pin.value(0)
en_pin.value(1)

# 設置步進方向
dir_pin.value(0)  # 1 為順時針，0 為逆時針

# 定義步進函數
def step(steps, delay):
    for _ in range(steps):
        step_pin.value(1)
        time.sleep(delay)
        step_pin.value(0)
        time.sleep(delay)

# 讓步進馬達轉動 200 步（假設每步 1.8 度，即一圈200步）
steps_per_revolution = 5
step_delay = 0.1  # 0.5s 延遲

step(steps_per_revolution, step_delay)

# 禁用步進馬達

