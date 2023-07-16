# import cv2 as cv
# print( cv.__version__ )

# import the opencv library
import cv2
import numpy as np
  
# define a video capture object
vid = cv2.VideoCapture(0)

i = 0
while(True):
      
    # capture the video frame
    # by frame
    ret, frame = vid.read()

    # conversion to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # conversion to HSV color space
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  
    # Display the resulting frames
    cv2.imshow('frame', frame)
    cv2.imshow('gray', gray)
    cv2.imshow('hsv_image', hsv_image)
      
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    print(i)
    i+=1
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()