import numpy as np
import cv2
import time 
import os

# path to trained classifiers
cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))
haar_model_face = os.path.join(cv2_base_dir, 'data/haarcascade_frontalface_default.xml')
haar_model_eye = os.path.join(cv2_base_dir, 'data/haarcascade_eye.xml')

# load trained classifiers
faceCascade = cv2.CascadeClassifier(haar_model_face)
eyeCascade = cv2.CascadeClassifier(haar_model_eye)

# capturing video through webcam
webcam = cv2.VideoCapture(0)

# change the resolution of the camera
# regular
# webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# wide
# webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

# prepare for time measurement
i = 0
last_time = time.time()

# start a while loop
while(True):

    # reading the video from the webcam in image frames
    _, imageFrame = webcam.read()
    # print(imageFrame.shape) # show window dimensions for testing purposes

    # conversion to grayscale
    gray = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2GRAY)

    # detect faces
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(50, 50)
    )
    for face in faces:
        x, y, w, h = face

        # detect eyes
        eyes = eyeCascade.detectMultiScale(gray[y: y+h//2, x:x+w], minNeighbors=5) # h//2 is to hide mouth

        # draw rectangle and add text for face
        imageFrame = cv2.rectangle(imageFrame, (x, y), 
                                    (x + w, y + h), 
                                    (0, 0, 255), 2)            
        cv2.putText(imageFrame, "Face", (x, y - 4),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                    (0, 0, 255))  
        # blur face
        # blur = cv2.blur(imageFrame[y: y+h, x:x+w], ksize=(50,50))
        # imageFrame[y: y+h, x:x+w] = blur

        # draw rectangle and add text for eyes
        for eye in eyes:
            ex, ey, ew, eh = eye
            imageFrame = cv2.rectangle(imageFrame, (x + ex, y + ey), 
                                    (x + ex + ew, y + ey + eh), 
                                    (0, 255, 0), 2)            
            cv2.putText(imageFrame, "Eye", (x + ex, y + ey - 4),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                    (0, 255, 0)) 

    # draw window
    cv2.imshow("Face Detection in Real-TIme", imageFrame)

    # measure time
    if time.time() > last_time + 1:
        last_time = time.time()
        print("FPS:" + str(i))
        i = 0
    else:
        i+=1

    # program termination
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# clean up
webcam.release()
cv2.destroyAllWindows()