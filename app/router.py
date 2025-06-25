"""
Main router
"""

from typing import Dict

from fastapi import Request, WebSocket, WebSocketDisconnect, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, StreamingResponse

from app import raspberry_board
from app.camera import camera
from app.raspi_functions import backward, forward, stop, turn_left, turn_right

templates = Jinja2Templates(directory="templates")
# WebSocket connections
active_connections: Dict[str, WebSocket] = {}

main_router = APIRouter()

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

    try:
        while True:
            data = await websocket.receive_text()

            # Handle keyboard commands
            if data == "KeyW":
                await forward()
            elif data == "KeyS":
                await backward()
            elif data == "KeyA":
                await turn_left()
            elif data == "KeyD":
                await turn_right()
            elif data == "KeySpace":
                stop()
            elif data == "KeyQ":
                # Example: Increase speed
                speed = min(100, speed + 10)
                raspberry_board.Ap.ChangeDutyCycle(speed)
                raspberry_board.Bp.ChangeDutyCycle(speed)
            elif data == "KeyE":
                # Example: Decrease speed
                speed = max(0, speed - 10)
                raspberry_board.Ap.ChangeDutyCycle(speed)
                raspberry_board.Bp.ChangeDutyCycle(speed)

    except WebSocketDisconnect:
        del active_connections[client_id]
        stop()  # Ensure robot stops if client disconnects
