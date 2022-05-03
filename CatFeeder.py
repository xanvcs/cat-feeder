#!/usr/bin/env python
# run these commands to update Pi to latest libraries
# sudo apt-get update
# sudo apt-get upgrade
# sudo apt-get install rpi.gpio

from GmailWrapper import GmailWrapper

import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

HOSTNAME = 'imap.gmail.com'
USERNAME = 'petfeeder569@gmail.com'
PASSWORD = 'Screwdesign1!'


def feedByGmail():
    gmailWrapper = GmailWrapper(HOSTNAME, USERNAME, PASSWORD)
    ids = gmailWrapper.getIdsBySubject('feed cats')
    if len(ids) > 0:
        try:
            feed()
            gmailWrapper.markAsRead(ids)
        except:
            print("Failed to feed pets, they're starvinggggg")


def feed():
    # let the GPIO library know where we've connected our servo to the Pi
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)

    try:
        servo = GPIO.PWM(18, 50)
        servo.start(12.5)

        # spin left, right, then left again rather than in a continuous circle
        # to prevent the food from jamming the servo
        servo.ChangeDutyCycle(2.5)
        time.sleep(10)
        servo.ChangeDutyCycle(12.5)
        time.sleep(2)
        servo.ChangeDutyCycle(2.5)
        time.sleep(7)
        
    finally:
        # always cleanup after ourselves
        servo.stop()
        GPIO.cleanup()


if __name__ == '__main__':
    # kick off the feeding process (move the servo)
    # we now use our new feedByGmail method to handle the feeding
    feedByGmail()
