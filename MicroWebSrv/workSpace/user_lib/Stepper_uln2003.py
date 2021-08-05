import time

# only test for uln2003
# spec: http://www.geeetech.com/wiki/index.php/Stepper_Motor_5V_4-Phase_5-Wire_%26_ULN2003_Driver_Board_for_Arduino#Interfacing_circuits
# driver web: https://github.com/zhcong/ULN2003-for-ESP32
class Stepper:
    # http://www.jangeox.be/2013/10/stepper-motor-28byj-48_25.html
    # from spec- Speed Variation Ratio ：1/64, the ratio between input wheel to output wheel is 64
    # from the spec (5.625'/64) angle for one HALF_STEP, and for one internal cycle you need 8 HALF_STEPs
    # so for 360' - (360/(5.625'/64))/8=512(befor any step) and multipy it by one cycle(8 HALF_STEPs or 4 FULL_STEPs)
    FULL_ROTATION = int(4075.7728395061727 / 8) # 512

    HALF_STEP = [
        [0, 0, 0, 1],
        [0, 0, 1, 1],
        [0, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 1, 0, 0],
        [1, 1, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 1],
    ]

    FULL_STEP = [
        [1, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 1, 0, 1],
        [1, 0, 0, 1]
    ]

    def __init__(self, mode, pin1, pin2, pin3, pin4, delayMs):
    	if mode=='FULL_STEP':
        	self.mode = self.FULL_STEP
        else:
        	self.mode = self.HALF_STEP
        self.pin1 = pin1
        self.pin2 = pin2
        self.pin3 = pin3
        self.pin4 = pin4
        self.delayMs = delayMs  # Recommend 10+ for FULL_STEP, 1 is OK for HALF_STEP
        
        # Initialize all to 0
        self.reset()
        
    def step(self, count, direction=1):
        """Rotate count steps. direction = -1 means backwards"""
        for x in range(count):
            for bit in self.mode[::direction]:
                self.pin1(bit[0])
                self.pin2(bit[1])
                self.pin3(bit[2])
                self.pin4(bit[3])
                time.sleep_ms(self.delayMs) # micropython fun
        self.reset()

    def angle(self, angle, direction=1):
        if angle < 0 : direction = -1
        if angle >= 0 : direction = 1
    	self.step(int(self.FULL_ROTATION * angle / 360), direction)

    def reset(self):
        # Reset to 0, no holding, these are geared, you can't move them
        self.pin1(0) 
        self.pin2(0) 
        self.pin3(0) 
        self.pin4(0)

    def create(pin1, pin2, pin3, pin4, delayMs=2, mode='HALF_STEP'):
	    return Stepper(mode, pin1, pin2, pin3, pin4, delayMs)

def tester( _callback = None):
    from machine import Pin, ADC
    from time import sleep
    POT_MAX_READ = 4095
    sliderPot = ADC(Pin(34))
    sliderPot.atten(ADC.ATTN_11DB) # Full range: 3.3v
    SETEPER_MAX_ANGLE = 360
    SETEPER_MIN_ANGLE = 0
    lastAngle = 0 # init angle=0'
    stepper = Stepper.create(Pin(13,Pin.OUT),Pin(12,Pin.OUT),Pin(14,Pin.OUT),Pin(27,Pin.OUT), delayMs=2)
    # stepper = Stepper.create(Pin(16,Pin.OUT),Pin(17,Pin.OUT),Pin(5,Pin.OUT),Pin(18,Pin.OUT), delayMs=2)
    try:
        while True:
            current_sliderPot = sliderPot.read() # min is 0, max read 4095
            # print(current_sliderPot)
            angle = current_sliderPot * SETEPER_MAX_ANGLE / POT_MAX_READ
            if not(angle == lastAngle):
                if angle < lastAngle: angle = -1*angle
                stepper.angle(angle) # set angle +/-
                print('angle is:', angle)# current_sliderPot * SERVO_MAX_ANGLE / POT_MAX_READ)
                lastAngle = abs(angle)
                if _callback:
                    _callback('angle is: ' + str(angle))
                sleep(15/1000) # 15ms time take the motor to get to position
            else: sleep(1/1000) # 1ms loop delay
    except KeyboardInterrupt : # control+C press
        pass

# use it
# import Stepper
# from machine import Pin
# Recommend 10ms+ for FULL_STEP, 1ms is OK for HALF_STEP, the defoult is HALF_STEP 
# s1 = Stepper.create(Pin(16,Pin.OUT),Pin(17,Pin.OUT),Pin(5,Pin.OUT),Pin(18,Pin.OUT), delayMs=2)
# s1.step(100) # 100 steps of 8 HALF_STEPs eche step, step mode(Full/Half) is init on create
# s1.step(100,-1) # backwards 100 steps of 8 HALF_STEPs eche step, step mode(Full/Half) is init on create
# s1.angle(180) # forwards 180', step mode(Full/Half) is init on create
# s1.angle(360,-1) # backwards 360', step mode(Full/Half) is init on create

# run tester - change potentiometer to change steper angle
# from user_lib.Stepper_uln2003 import tester
# from user_lib.display_msg import display
# tester(display)