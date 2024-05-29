from machine import Pin
from servo import Servo

class ServoController:
    def __init__(self):
        self.servo_1 = Servo(pin_id=1)
        self.servo_2 = Servo(pin_id=2)
        self.servo_3 = Servo(pin_id=3)
        self.servo_4 = Servo(pin_id=4)
        self.servo_5 = Servo(pin_id=5)
        self.servo_6 = Servo(pin_id=6)
        self.servo_1.write(0)
        self.servo_2.write(0)
        self.servo_3.write(0)
        self.servo_4.write(0)
        self.servo_5.write(0)
        self.servo_6.write(0)
        
        self.servo_degrees = {
            'servo_1': 0,
            'servo_2': 0,
            'servo_3': 0,
            'servo_4': 0,
            'servo_5': 0,
            'servo_6': 0
        }
        

#----
#class ServoController:
#    def __init__(self, pin_ids):
#        self.servos = {f'servo_{i+1}': Servo(pin_id) for i, pin_id in enumerate(pin_ids)}
#        self.servo_degrees = {key: 0 for key in self.servos}
#
#        for servo in self.servos.values():
#            servo.write(0)       
#----

    def set_servo_angle(self, servo_id, degree):
        if servo_id in self.servo_degrees:
            getattr(self, servo_id).write(degree)
            self.servo_degrees[servo_id] = degree
            if round(degree) != round(getattr(self, servo_id).read()):
                print(f'{servo_id}degree check: failed')
#                 print(f'{servo_id}degree check: passed')
                #print(type(self.servo_degrees[servo_id]))
                #print(self.servo_degrees[servo_id])
                #print(type(round(getattr(self, servo_id).read())))
                #print(round(getattr(self, servo_id).read()))
#             else:
#                 print(f'{servo_id}degree check: failed')
                #print(type(self.servo_degrees[servo_id]))
                #print(self.servo_degrees[servo_id])
                #print(type(round(getattr(self, servo_id).read())))
                #print(round(getattr(self, servo_id).read()))

            

    def get_servo_degrees(self):
        return self.servo_degrees
    
servo_controller = ServoController()
