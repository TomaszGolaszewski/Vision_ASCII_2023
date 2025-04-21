# Ascii view offline demo 2023
# By Tomasz Golaszewski
# 07.2023

# Quick project to check OpenCV Library by preparing the camera with ascii view

import cv2
import os

from main_ascii_camera import draw_in_terminal


def run():
# main function

    # reading the image from disk
    imageFrame = cv2.imread(os.path.join("imgs", "my_cat.jpg"), cv2.IMREAD_COLOR)

    # calculate terminal view dimensions
    # letters 9x11
    # grid in terminal 9x20
    # photo (960, 1290)
    # camera (480, 640) 
    scale_console = 0.75
    scale_preview = 0.6
    image_height, image_width, _ = imageFrame.shape
    width = int(scale_console * image_width // 9)
    height = int(scale_console * image_height // 20)

    # conversion to grayscale and resize to fit terminal
    gray = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2GRAY)
    resize_img_console = cv2.resize(gray, (width, height))
    resize_img_preview = cv2.resize(gray, (int(scale_preview * image_width), int(scale_preview * image_height)))

    # draw window
    draw_in_terminal(resize_img_console)
    cv2.imshow("Camera preview", resize_img_preview)

    # program termination
    cv2.waitKey(0)

    # clean up
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run()