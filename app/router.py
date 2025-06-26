"""
Main router
"""

from typing import Dict

from fastapi import Request, WebSocket, WebSocketDisconnect, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, StreamingResponse


from app.camera import camera
from app.params import SPEED, TURN_FACTOR
from app.raspi_functions import stop, set_motor_speeds

templates = Jinja2Templates(directory="templates")
# WebSocket connections
active_connections: Dict[str, WebSocket] = {}

main_router = APIRouter()
base_speed = SPEED
current_speeds = {"left": 0, "right": 0}

@main_router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Get main page.
    """

    return templates.TemplateResponse("index.html", {"request": request})

@main_router.get("/video_feed")
async def video_feed():
    """
    Feed the webcam.
    """

    return StreamingResponse(camera.generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@main_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Mowing the robot.
    """
    await websocket.accept()
    client_id = str(id(websocket))
    active_connections[client_id] = websocket

    # Track which keys are currently pressed
    active_keys = set()

    try:
        while True:
            data = await websocket.receive_text()
            global base_speed
            # Update active keys
            if data.startswith("Key"):
                if data.endswith("Down"):
                    key = data[3:-4]
                    active_keys.add(key)
                elif data.endswith("Up"):
                    key = data[3:-2]
                    active_keys.discard(key)

            # Calculate motor speeds based on active keys
            left_speed = 0
            right_speed = 0

            if "W" in active_keys:
                left_speed = base_speed
                right_speed = base_speed

                # Apply turning if needed
                if "A" in active_keys:  # Turn left
                    right_speed = base_speed
                    left_speed = base_speed * (1 - TURN_FACTOR)
                elif "D" in active_keys:  # Turn right
                    left_speed = base_speed
                    right_speed = base_speed * (1 - TURN_FACTOR)

            elif "S" in active_keys:
                left_speed =  -base_speed
                right_speed =  -base_speed

                # Apply turning if needed
                if "A" in active_keys:  # Turn left while reversing
                    right_speed =  -base_speed
                    left_speed =  -base_speed * (1 - TURN_FACTOR)
                elif "D" in active_keys:  # Turn right while reversing
                    left_speed =  -base_speed
                    right_speed =  -base_speed * (1 - TURN_FACTOR)

            # Handle standalone turns
            elif "A" in active_keys:
                left_speed =  -base_speed * TURN_FACTOR
                right_speed = base_speed * TURN_FACTOR
            elif "D" in active_keys:
                left_speed = base_speed * TURN_FACTOR
                right_speed =  -base_speed * TURN_FACTOR

            # Update speed if Q/E pressed
            if "Q" in active_keys:
                base_speed = min(100, base_speed + 5)
            if "E" in active_keys:
                base_speed = max(5, base_speed - 5)

            # Apply the calculated speeds
            global current_speeds
            if left_speed != current_speeds["left"] or right_speed != current_speeds["right"]:
                set_motor_speeds(left_speed, right_speed)
                current_speeds["left"] = left_speed
                current_speeds["right"] = right_speed

                # Send speed update to all connected clients
                for connection in active_connections.values():
                    try:
                        await connection.send_text(f"SPEED:{left_speed}:{right_speed}")
                    except:
                        continue

    except WebSocketDisconnect:
        del active_connections[client_id]
        stop()  # Ensure robot stops if client disconnects
