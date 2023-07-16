import numpy as np
import cv2
import time 
  
# capturing video through webcam
webcam = cv2.VideoCapture(0)

# prepare for time measurement
i = 0
last_time = time.time()

# start a while loop
while(True):

    # reading the video from the webcam in image frames
    _, imageFrame = webcam.read()
    # print(imageFrame.shape) # show window dimensions for testing purposes # (480, 640, 3)

    # convert the imageFrame in BGR (RGB color space) to HSV (hue-saturation-value color space) 
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
  
    # set range for red color and define mask
    red_lower = np.array([136, 87, 111], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
    cv2.imshow('red_mask', red_mask) # show window for testing purposes
    # print(red_mask.shape) # show window dimensions for testing purposes # (480, 640)

    # morphological transform, dilation for each color and bitwise_and operator
    # between imageFrame and mask determines to detect only that particular color
    kernel = np.ones((5, 5), "uint8")

    # for red color
    red_mask = cv2.dilate(red_mask, kernel)
    cv2.imshow('red_mask_2', red_mask) # show window for testing purposes
    res_red = cv2.bitwise_and(imageFrame, imageFrame, 
                              mask = red_mask)
    cv2.imshow('res_red', res_red) # show window for testing purposes

    # creating contour to track red color
    contours, hierarchy = cv2.findContours(red_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
      
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 5000):
            x, y, w, h = cv2.boundingRect(contour)
            center_coordinates = (x+w//2, y+h//2)
            print(center_coordinates)
            # draw rectangle
            imageFrame = cv2.rectangle(imageFrame, (x, y), 
                                       (x + w, y + h), 
                                       (0, 0, 255), 2)
            # draw circle
            imageFrame = cv2.circle(imageFrame, center_coordinates, 20, (0, 0, 255), 2)

            # draw lines
            l = 50
            imageFrame = cv2.line(imageFrame, (x+w//2 - l, y+h//2), (x+w//2 + l, y+h//2), (0, 0, 255), 2) # -
            imageFrame = cv2.line(imageFrame, (x+w//2, y+h//2 - l), (x+w//2, y+h//2 + l), (0, 0, 255), 2) # |

            # draw text              
            cv2.putText(imageFrame, "Red Colour", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                        (0, 0, 255))   
            
    # draw window
    cv2.imshow("Red Color Detection in Real-TIme", imageFrame)

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

webcam.release()
cv2.destroyAllWindows()