#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import schedule

GPIO_PIN =17

FREQUENCY = 50
MIN_DUTY = 2.2
MAX_DUTY = 7.5
SLEEP_DURATION = 0.8

def feed(t):
    print(t)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_PIN, GPIO.OUT)
    
    try:
        servo = GPIO.PWM(GPIO_PIN, FREQUENCY)
        servo.start(MIN_DUTY)

        for index in range(0, 3):
            dutyCycle = MIN_DUTY if (index % 2 == 0) else MAX_DUTY
            servo.ChangeDutyCycle(dutyCycle)
            time.sleep(SLEEP_DURATION)
    finally:
        # Pulses to reset servo to prevent buzzing
        servo.ChangeDutyCycle(MAX_DUTY + 0.1)
        time.sleep(SLEEP_DURATION)

        servo.ChangeDutyCycle(MAX_DUTY - 0.1)
        time.sleep(SLEEP_DURATION)
        
        servo.stop()
        GPIO.cleanup()
            
if __name__ == '__main__':
    print("Starting program")
    
    feeding_schedule = ["06:00", "17:00", "21:00"]
    
    for t in feeding_schedule:
        print("Scheduling a feeding at %s." % t)
        schedule.every().day.at(t).do(feed, "Feeding Miso at %s" % t)
    
    while True:
        schedule.run_pending()
        time.sleep(60)
        