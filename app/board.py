"""
Board class.
"""

import RPi.GPIO as GPIO

from app.params import SPEED


class Board:
    """
    Used to define the used pins
    """

    # Motor pins
    Apin1 = 15
    Apin2 = 14
    Bpin1 = 26
    Bpin2 = 19
    Aen = 18   # PWM pin
    Ben = 13   # PWM pin
    stateLED = 25

    def __init__(self):
        # Setup GPIO pins
        GPIO.setup(self.Apin1, GPIO.OUT)
        GPIO.setup(self.Apin2, GPIO.OUT)
        GPIO.setup(self.Bpin1, GPIO.OUT)
        GPIO.setup(self.Bpin2, GPIO.OUT)
        GPIO.setup(self.Aen, GPIO.OUT)
        GPIO.setup(self.Ben, GPIO.OUT)
        GPIO.setup(self.stateLED, GPIO.OUT)

        # Initialize PWM
        self.Ap = GPIO.PWM(self.Aen, 1000)  # Left side
        self.Bp = GPIO.PWM(self.Ben, 1000)  # Right side
        self.Ap.start(SPEED)
        self.Bp.start(SPEED)
