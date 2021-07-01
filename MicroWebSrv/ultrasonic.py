
# import ultrasonic
from machine import Pin, time_pulse_us
from time import sleep

led = Pin(32, Pin.OUT)
echoPin = Pin(35, Pin.IN)
trigPin = Pin(33, Pin.OUT)

while True:
    trigPin.off() # digitalWrite(trigPin, LOW);
    sleep(2/1000000) # delayMicroseconds(2);

    # Sets the trigPin on HIGH state for 10 micro seconds
    trigPin.on() # digitalWrite(trigPin, HIGH);
    sleep(10/1000000) # delayMicroseconds(10);
    trigPin.off() # digitalWrite(trigPin, LOW);

    # Reads the echoPin, returns the sound wave travel time in microseconds
    duration = time_pulse_us(echoPin, 1) # pulseIn(echoPin, HIGH);

    # Calculating the distance
    distance= duration*0.034/2

    # Prints the distance on the Serial Monitor
    print('Distance: ', round(distance)) # Serial.print("Distance: ");

    sleep(1/10)