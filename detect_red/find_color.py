# -*- coding: utf-8 -*-

import cv2
import numpy as np
import glob

# color definition

RED   = 1
GREEN = 2
BLUE  = 3
REDTAPE = 4


def find_rect_of_target_color(image, color_type)->list:
    """_summary_

    Args:
        image (_type_): _description_opencv file
        color_type (_type_): _description_RED   = 1
        GREEN = 2
        BLUE  = 3

    Returns:
        _type_: _description_
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)
    h = hsv[:, :, 0]
    s = hsv[:, :, 1]

    # red detection
    if color_type == REDTAPE:
        mask = np.zeros(h.shape, dtype=np.uint8)
        mask[((h < 20) | (h > 200)) & (s > 128)] = 255

        

    # red detection
    if color_type == RED:
        mask = np.zeros(h.shape, dtype=np.uint8)
        mask[((h < 20) | (h > 200)) & (s > 128)] = 255

    # blue detection
    if color_type == BLUE:
        lower_blue = np.array([130, 50, 50])
        upper_blue = np.array([200, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # green detection
    if color_type == GREEN:
        lower_green = np.array([75, 50, 50])
        upper_green = np.array([110, 255, 255])
        mask = cv2.inRange(hsv, lower_green, upper_green)

    # 近傍の定義
    neiborhood = np.array([[0, 1, 0],
                            [1, 1, 1],
                            [0, 1, 0]],
                            np.uint8)
    # 収縮
    mask = cv2.dilate(mask,
                        neiborhood,
                        iterations=2)

    # 膨張
    mask = cv2.erode(mask,
                    neiborhood,
                    iterations=2)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    rects = []
    for contour in contours:
        approx = cv2.convexHull(contour)
        rect = cv2.boundingRect(approx)
        rects.append(np.array(rect))

    return len(contours)
    
