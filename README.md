# Raspberry Pi Robot Controller

A FastAPI-based web controller for a Raspberry Pi-powered robot with live video streaming and keyboard control capabilities.

## Table of Contents
1. [Features](#features)
2. [Hardware Requirements](#hardware-requirements)
3. [Software Requirements](#software-requirements)  
4. [Installation](#installation)
5. [Usage](#usage)
6. [Project Structure](#structure)
7. [Configuration](#configuration)
8. [Safety Features](#safety-features)

## Features <a id="features"></a>

- 🎮 Web-based control interface with keyboard controls (WASD)
- 📹 Live video streaming from the robot's camera
- ⚡ Real-time motor control with adjustable speed
- 🔌 GPIO management for motors and shutdown button
- 🌐 WebSocket communication for responsive controls
- 🔋 Safe shutdown functionality via hardware button

## Hardware Requirements <a id="hardware-requirements"></a>

- Raspberry Pi (tested on RPi 4)
- Motor controller board (L298N or similar)
- 2 DC motors with wheels
- Webcam or Raspberry Pi camera module
- Power supply
- Optional: Shutdown button connected to GPIO 21

## Software Requirements <a id="software-requirements"></a>

- Python 3.7+
- Raspberry Pi OS
- FastAPI
- Uvicorn
- OpenCV
- RPi.GPIO

## Installation <a id="installation"></a>

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/robokos.git
   cd robokos
   ```
   
2. Install dependencies
   ```bash
   poetry install
   ```
   
## Usage <a id="usage"></a>
Running on local network
```bash
cd folder-of-project
python main.py
```
Now you can use it on localnetwork at 8030 port

## Project Structure <a id="structure"></a>
```
remotecar/
├── app/
│   ├── board.py          # GPIO and motor control setup
│   ├── camera.py         # Video capture and streaming
│   ├── params.py         # Configuration parameters
│   ├── raspi_functions.py # Motor control functions
│   └── router.py         # FastAPI routes and WebSocket
├── static/               # Static files (CSS, JS, images)
├── templates/            # HTML templates
├── main.py               # Application entry point
└── README.md             # This file
```

## Configuration <a id="configuration"></a>
Edit app/params.py to adjust:
  - Motor speeds
  - Turning factors
  - Camera resolution

## Safety Features <a id="safety-features"></a>
Automatic motor stop on WebSocket disconnect
  - Hardware shutdown button
  - Proper GPIO cleanup on exit
