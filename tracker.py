import cv2
import time
from communication import *

from roboflow import Roboflow

rf = Roboflow(api_key="tJUOl22WsAVuNvN5vkhu")
project = rf.workspace("cameratracker-kxcvn").project("colibritracker")
model = project.version(1, local="http://localhost:9001/").model

# Initialize the camera (force V4L2 backend)
camera = cv2.VideoCapture(0, cv2.CAP_V4L2)
teensyInit()

# Check if the camera opened successfully
if not camera.isOpened():
    print("Error: Could not open the camera.")
    exit()

last_time = time.time()

# Continuous loop for face detection
try:
    while True:
        # Compute and print fps
        # print("FPS: ", 1 / (time.time() - last_time))

        # Capture a single frame
        ret, frame = camera.read()
        last_time = time.time()
        
        # Reduce the frame size to speed up the detection
        frame = cv2.resize(frame, (640, 360))
        # Check if the frame was captured correctly
        if not ret:
            print("Error: Failed to capture image")
            break
        # Encode the frame as a JPEG image
        _, jpeg = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
        
        # Save the image to a png file, delete the previous file if it already exists
        with open("frame.jpg", "wb") as f:
            f.write(jpeg.tobytes())

        prediction = model.predict("frame.jpg", confidence=40, overlap=30)
        
        # Print the center coordinates of the detected object
        
        # Result of the json is often the form: 
        #{'predictions': [{'x': 309.0, 'y': 170.0, 'width': 66.0, 'height': 158.0, 'confidence': 0.8635298013687134, 'class': 'rocket', 'image_path': 'frame.jpg', 'prediction_type': 'ObjectDetectionModel'}], 'image': {'width': '640', 'height': '480'}}
        #{'predictions': [], 'image': {'width': '640', 'height': '480'}}
        
        if prediction.json()["predictions"]:
            x = (prediction.json()["predictions"][0]["x"] + prediction.json()["predictions"][0]["width"] / 2)-320
            y = (prediction.json()["predictions"][0]["y"] + prediction.json()["predictions"][0]["height"] / 2)-180
            print("Center coordinates: ({}, {})".format(x, y))
            
            # Send the target point to the Teensy
            pointToSend = LightPoint("rocket", True, x, y, time.time()-last_time)
            sendTargetToTeensy(pointToSend,33,5.0,10)
        else:
            print("No object detected.")
            pointToSend = LightPoint("rocket", False, 0, 0, time.time()-last_time)
            sendTargetToTeensy(pointToSend,33,5.0,10)
        

except KeyboardInterrupt:
    print("Detection loop interrupted.")

# Release the camera
camera.release()