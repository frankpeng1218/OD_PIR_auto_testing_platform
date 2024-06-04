from machine import Pin
from servo import Servo

class ServoController:
    def __init__(self):
        # Read initial servo positions from the file
        self.servo_degrees = self.read_servo_values_from_file()
#         print(self.servo_degrees)

        # Initialize servos
        self.servo_1 = Servo(pin_id=1)
        self.servo_2 = Servo(pin_id=2)
        self.servo_3 = Servo(pin_id=3)
        self.servo_4 = Servo(pin_id=4)
        self.servo_5 = Servo(pin_id=5)
        self.servo_6 = Servo(pin_id=6)

        # Set initial positions
        self.servo_1.write(self.servo_degrees['servo_1'])
        self.servo_2.write(self.servo_degrees['servo_2'])
        self.servo_3.write(self.servo_degrees['servo_3'])
        self.servo_4.write(self.servo_degrees['servo_4'])
        self.servo_5.write(self.servo_degrees['servo_5'])
        self.servo_6.write(self.servo_degrees['servo_6'])
        
        
        # 计算每一步的减少量
        steps = 50
        reductions = {key: value / steps for key, value in self.servo_degrees.items()}
        # 逐步减少角度直到归0
        for step in range(steps):
            for key in self.servo_degrees:
                self.servo_degrees[key] -= reductions[key]
                if self.servo_degrees[key] < 0:
                    self.servo_degrees[key] = 0
            
            # 更新舵机角度
            self.set_servo_angle(servo_id = 'servo_1', degree = self.servo_degrees['servo_1'])
            self.set_servo_angle(servo_id = 'servo_2', degree = self.servo_degrees['servo_2'])
            self.set_servo_angle(servo_id = 'servo_3', degree = self.servo_degrees['servo_3'])
            self.set_servo_angle(servo_id = 'servo_4', degree = self.servo_degrees['servo_4'])
            self.set_servo_angle(servo_id = 'servo_5', degree = self.servo_degrees['servo_5'])
            self.set_servo_angle(servo_id = 'servo_6', degree = self.servo_degrees['servo_6'])
        
    
    def read_servo_values_from_file(self):
        servo_values = {}
        try:
            with open('servo_value.txt', 'r') as file:
                values = file.read().strip().split()
                servo_values = {
                    'servo_1': int(values[0]),
                    'servo_2': int(values[1]),
                    'servo_3': int(values[2]),
                    'servo_4': int(values[3]),
                    'servo_5': int(values[4]),
                    'servo_6': int(values[5])
                }
        except Exception as e:
            print(f"Error reading servo values: {e}")
            # Set default values if the file cannot be read
            servo_values = {
                'servo_1': 0,
                'servo_2': 0,
                'servo_3': 0,
                'servo_4': 0,
                'servo_5': 0,
                'servo_6': 0
            }
        return servo_values

    def write_servo_values_to_file(self):
        try:
            with open('servo_value.txt', 'w') as file:
                file.write(' '.join(str(self.servo_degrees[f'servo_{i+1}']) for i in range(6)))
        except Exception as e:
            print(f"Error writing servo values: {e}")

    def set_servo_angle(self, servo_id, degree):
        if servo_id in self.servo_degrees:
            getattr(self, servo_id).write(degree)
            self.servo_degrees[servo_id] = degree
            self.write_servo_values_to_file()
            if round(degree) != round(getattr(self, servo_id).read()):
                print(f'{servo_id} degree check: failed')

    def get_servo_degrees(self):
        return self.servo_degrees

# Example usage
# servo_controller = ServoController()
# servo_controller.set_servo_angle('servo_1', 40)
# print(servo_controller.get_servo_degrees())

