"""
Functions for controlling.
"""

import time
import os

import RPi.GPIO as GPIO

from app.camera import camera
from app.board import Board


async def shutdownrpi():
    """
    Used to shutdown the system with a button, connected to the board.
    """

    print("Shutting down")
    time.sleep(5)
    os.system("sudo shutdown -h now")

def cleanup():
    """
    Clean before finish session.
    """

    stop()
    GPIO.cleanup()
    camera.shutdown()

# Motor control functions
async def forward():
    """
    Moving Forward
    """

    GPIO.output(Board.Apin1, GPIO.LOW)
    GPIO.output(Board.Apin2, GPIO.HIGH)
    GPIO.output(Board.Bpin1, GPIO.LOW)
    GPIO.output(Board.Bpin2, GPIO.HIGH)
    # print("Moving Forward")

async def backward():
    """
    Moving Backward
    """

    GPIO.output(Board.Bpin1, GPIO.HIGH)
    GPIO.output(Board.Bpin2, GPIO.LOW)
    GPIO.output(Board.Apin1, GPIO.HIGH)
    GPIO.output(Board.Apin2, GPIO.LOW)
    # print("Moving Backward")

def stop():
    """
    Stopping
    """

    GPIO.output(Board.Apin1, GPIO.HIGH)
    GPIO.output(Board.Apin2, GPIO.HIGH)
    GPIO.output(Board.Bpin1, GPIO.HIGH)
    GPIO.output(Board.Bpin2, GPIO.HIGH)
    # print("Stopping")

async def turn_left():
    """
    Turning Left
    """

    GPIO.output(Board.Bpin1, GPIO.LOW)
    GPIO.output(Board.Bpin2, GPIO.HIGH)  # Right side forward
    GPIO.output(Board.Apin1, GPIO.HIGH)
    GPIO.output(Board.Apin2, GPIO.LOW)   # Left side backward
    # print("Turning Left")

async def turn_right():
    """
    Turning Right
    """

    GPIO.output(Board.Apin1, GPIO.LOW)
    GPIO.output(Board.Apin2, GPIO.HIGH)  # Left side forward
    GPIO.output(Board.Bpin1, GPIO.HIGH)
    GPIO.output(Board.Bpin2, GPIO.LOW)   # Right side backward
    # print("Turning Right")
