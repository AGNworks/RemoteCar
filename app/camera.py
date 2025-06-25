"""
Camera
"""

import asyncio
import cv2


class Camera:
    """
    Class to control the camera object.
    """

    def __init__(self):
        # Webcam setup
        self.camera_object = cv2.VideoCapture(0)
        self.camera_object.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.camera_object.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    def shutdown(self):
        """
        Disconnect.
        """
        self.camera_object.release()

    async def generate_frames(self):
        """
        Get frames from camera.
        """

        while True:
            success, frame = self.camera_object.read()
            if not success:
                break
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            await asyncio.sleep(0.03)  # Control frame rate


camera = Camera()
