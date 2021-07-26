# the micro servo 9g, need external power supply for the motor and the grnd connected to esp32 grnd
# brown = grnd, red = 5v, yellow = signal
# micro servo PWM freq=50, dutycycle[30=0', 140=180']
from machine import Pin, ADC, PWM
from time import sleep

servo = PWM(Pin(4), freq=50) # 50HZ = 20ms cycle
SERVO_MAX_ANGLE = 180
SERVO_MIN_ANGLE = 0
SERVO_MAX_DUTY = 140 # angle=180'
SERVO_MIN_DUTY = 30 # angle=0'
SERVO_RANG_DUTY = SERVO_MAX_DUTY - SERVO_MIN_DUTY
POT_MAX_READ = 4095
sliderPot = ADC(Pin(34))
sliderPot.atten(ADC.ATTN_11DB) # Full range: 3.3v
lastDuty = SERVO_MIN_DUTY # init angle=0'
try:
    while True:
        current_sliderPot = sliderPot.read() # min is 0, max read 4095
        # print(current_sliderPot)
        calcPotDuty = int(SERVO_MIN_DUTY + SERVO_RANG_DUTY * current_sliderPot / POT_MAX_READ)
        if not(calcPotDuty == lastDuty or calcPotDuty == lastDuty + 1  \
            or calcPotDuty == lastDuty - 1):
            lastDuty = calcPotDuty
            servo.duty(calcPotDuty)
            print('angle is:', current_sliderPot * SERVO_MAX_ANGLE / POT_MAX_READ)
            sleep(15/1000) # 15ms time take the motor to get to position
        else: sleep(1/1000) # 1ms loop delay
except KeyboardInterrupt : # control+C press
    pass
servo.deinit()
