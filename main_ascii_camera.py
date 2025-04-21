# Ascii view 2023
# By Tomasz Golaszewski
# 07.2023

# Quick project to check OpenCV Library by preparing the camera with ascii view

import numpy as np
import cv2
import time 
import os

def get_letter_by_density(number):
# convert number in range (0, 255) into letter by pixel density
    density_standard = "Ñ@#W$9876543210?!abc;:+=-,._ "
    lenght_of_standard = len(density_standard)
    # i = number * (lenght_of_standard - 1) // 255 # negative image
    i = lenght_of_standard - number * (lenght_of_standard - 1) // 255 - 1
    letter = density_standard[i]
    return letter


def draw_in_terminal(table):
# draw in terminal

    # check the system and clear terminal
    if os.name == "posix":
        os.system('clear')
        # print("Linux")
    elif os.name == "nt":
        os.system('cls')
        # print("Windows")
    else:
        os.system('cls')
        # print("other")

    for row in table:
        new_row = ""
        for pixel in row:
            new_row += get_letter_by_density(pixel)
        print(new_row)
    print("")


def run():
# main function

    # capturing video through webcam
    webcam = cv2.VideoCapture(0)

    # prepare for time measurement
    i = 0
    last_time = time.time()

    # calculate terminal view dimensions
    # letters 9x11
    # grid in terminal 9x20
    # camera (480, 640) 
    scale = 1.5
    width = int(scale * 640 // 9)
    height = int(scale * 480 // 20)

    # start a while loop
    while(True):

        # reading the video from the webcam in image frames
        _, imageFrame = webcam.read()

        # conversion to grayscale and resize to fit terminal
        gray = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2GRAY)
        resize_img = cv2.resize(gray , (width, height))

        # draw window
        draw_in_terminal(resize_img)
        cv2.imshow("Camera preview", gray)

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


if __name__ == "__main__":
    run()