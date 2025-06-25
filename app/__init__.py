"""
Board set ups.
"""

import RPi.GPIO as GPIO

from app.board import Board
from app.raspi_functions import shutdownrpi


# Initialize GPIO
GPIO.setmode(GPIO.BCM)

## SHUTDOWN
# Setup shutdown button
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Add Shutdown event
GPIO.add_event_detect(21, GPIO.FALLING, callback=shutdownrpi, bouncetime=2000)

# Set up the raspberry board
raspberry_board = Board()
