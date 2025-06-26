"""
Functions for controlling.
"""

import RPi.GPIO as GPIO

from app.camera import camera
from app.board import Board, raspberry_board
from app.params import MAX_SPEED, MIN_SPEED

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

def set_motor_speeds(left_speed, right_speed):
    """
    Set the motor speeds.
    """

    # Get the speed to set
    if abs(left_speed) > MAX_SPEED:
        v_left = MAX_SPEED
    elif abs(left_speed) < MIN_SPEED:
        v_left = MIN_SPEED
    else:
        v_left = abs(left_speed)

    if abs(right_speed) > MAX_SPEED:
        r_left = MAX_SPEED
    elif abs(right_speed) < MIN_SPEED:
        r_left = MIN_SPEED
    else:
        r_left = abs(right_speed)

    # Set the speed
    raspberry_board.Ap.ChangeDutyCycle(v_left)
    raspberry_board.Bp.ChangeDutyCycle(r_left)

    # Set the direction
    if left_speed < 0:
        GPIO.output(Board.Apin1, GPIO.HIGH)
        GPIO.output(Board.Apin2, GPIO.LOW)   # Left side backward
    else:
        GPIO.output(Board.Apin1, GPIO.LOW)
        GPIO.output(Board.Apin2, GPIO.HIGH)  # Left side forward

    if right_speed < 0:
        GPIO.output(Board.Bpin1, GPIO.HIGH)
        GPIO.output(Board.Bpin2, GPIO.LOW)   # Right side backward
    else:
        GPIO.output(Board.Bpin1, GPIO.LOW)
        GPIO.output(Board.Bpin2, GPIO.HIGH)  # Right side forward
