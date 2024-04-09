import serial
from ultralytics import YOLO
import cv2
import math

# Load video
video_path = 'C:/Users/SUCCESS/Desktop/3.2_Project/Photo Album2.mp4' # Replace with your video file path
cap = cv2.VideoCapture(video_path)

# Check if video opened successfully
if not cap.isOpened():
    print("Error opening video file")

# Initialize serial communication
ser = serial.Serial('COM6', 9600)  # Replace 'COM5' with the correct port

# model
model = YOLO("C:/Users/SUCCESS/Desktop/3.2_Project/file (3)/kaggle/working/runs/detect/train/weights/best.pt") # Ensure the model path is correct

classNames = ['0', '1', '10', '11', '2', '3', '4', '5', '6', '7', '8', '9']

min_confidence = 0.7  # Set your desired threshold (e.g., 0.5 for 50%)

while cap.isOpened():
    success, img = cap.read()
    if not success:
        break

    # Initialize t to 0
    t = 0

    results = model(img, stream=True)

    # coordinates
    for r in results:
        boxes = r.boxes

        for box in boxes:
            confidence = math.ceil((box.conf[0] * 100)) / 100

            if confidence >= min_confidence:
                # Set t to 1 if object is detected
                t = 1

                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

                cls = int(box.cls[0])
                print("Class name -->", classNames[cls])

                org = (x1, y1)
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                color = (255, 0, 0)
                thickness = 2

                cv2.putText(img, f"{classNames[cls]} {confidence:.2f}", org, font, fontScale, color, thickness)
            
            
            else :
              t=0
    # Seqnd the value of t through serial communication to Arduino
    ser.write(str(t).encode('utf-8'))

    # Now, you can use the value of t as needed
    print("t =", t)

    cv2.imshow('Video', img)
    if cv2.waitKey(1) == ord('q'):
        break

# Close the serial connection and release video capture
ser.close()
cap.release()