# camera/camera_handler.py

import cv2
import threading
import time
from ultralytics import YOLO
from utils.config import CAMERA_INDEX, MODEL_PATH, CONFIDENCE_THRESHOLD

model = YOLO(MODEL_PATH)
latest_frame = None
camera_event = threading.Event()
frame_lock = threading.Lock()

def camera_loop(detection_callback):
    global latest_frame
    cap = cv2.VideoCapture(CAMERA_INDEX)

    while camera_event.is_set():
        ret, frame = cap.read()
        if not ret:
            continue

        results = model.predict(source=frame, conf=CONFIDENCE_THRESHOLD, verbose=False)
        annotated = results[0].plot()
        classes = results[0].boxes.cls.tolist()
        names = results[0].names

        # Send to detection alert logger
        for cls_id in classes:
            label = names[int(cls_id)]
            detection_callback(label)

        with frame_lock:
            latest_frame = annotated

        time.sleep(0.05)

    cap.release()

def start_camera(detection_callback):
    if not camera_event.is_set():
        camera_event.set()
        threading.Thread(target=camera_loop, args=(detection_callback,), daemon=True).start()

def stop_camera():
    camera_event.clear()

def get_latest_frame():
    with frame_lock:
        return latest_frame
