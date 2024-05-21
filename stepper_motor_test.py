# Frank_edited_0521_stepper motor test
# the test includes the TLP281-4 module and ULN2003AN stepper motor 


import utime
from machine import Pin

in1 = Pin(2, Pin.OUT, value=0)
in2 = Pin(3, Pin.OUT, value=0)
in3 = Pin(4, Pin.OUT, value=0)
in4 = Pin(5, Pin.OUT, value=0)

# 定義每個步進的序列
forward_seq = [[1, 0, 0, 1],
               [1, 0, 0, 0],
               [1, 1, 0, 0],
               [0, 1, 0, 0],
               [0, 1, 1, 0],
               [0, 0, 1, 0],
               [0, 0, 1, 1],
               [0, 0, 0, 1]]

backward_seq = list(reversed(forward_seq))

def set_step(step, seq):
    in1.value(seq[step][0])
    in2.value(seq[step][1])
    in3.value(seq[step][2])
    in4.value(seq[step][3])

def forward(delay, steps):
    for i in range(steps):
        for step in range(8):
            set_step(step, forward_seq)
            utime.sleep_ms(delay)

def backward(delay, steps):
    for i in range(steps):
        for step in range(8):
            set_step(step, backward_seq)
            utime.sleep_ms(delay)
            
            
            
# 初始化步进电机
def init_stepper():
    # 设置步进电机为初始状态
    set_step(0, forward_seq)

    # 设置步进电机转速（延时）
    delay = 5  # 设置延时，可以根据步进电机的特性调整

    return delay



# 控制步進馬達
while True:
   forward(5, 50)  # 前進50步
   utime.sleep(1)
   backward(5, 50)  # 後退50步
   utime.sleep(1)
