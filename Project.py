# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 12:33:57 2021

@author: laksh
"""

import cv2
import pyautogui
import numpy as np

def nothing(x):
    pass

cv2.namedWindow('DIP')

vid = cv2.VideoCapture(0);
prev_pos = "neutral"

while True:
    _,frame = vid.read()
    
    frame = cv2.flip(frame, 1)
    frame = cv2.GaussianBlur(frame, (5,5), 0)
    
    lower = np.array([49, 0, 125])
    upper = np.array([121, 255, 255])
    mask = cv2.inRange(frame, lower, upper)
    
    _,thresh = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours)==0:
        continue
    max_contour = max(contours, key = cv2.contourArea)
    
    epsilon = 0.01*cv2.arcLength(max_contour,True)
    max_contour = cv2.approxPolyDP(max_contour,epsilon,True)
    
    M =cv2.moments(max_contour)
    try:
        x = int(M['m10']/M['m00'])
        y = int(M['m01']/M['m00'])
    except ZeroDivisionError:
        continue
    
    frame = cv2.circle(frame, (x, y), 10, (0, 255, 255), 2)
    frame = cv2.drawContours(frame, [max_contour], -1, (0, 0, 255), 2)
    frame = cv2.line(frame, (200, 300), (360, 300), (0, 0, 255), 2)
    frame = cv2.line(frame, (360, 0), (360, 640), (0, 0, 255), 2)
    frame = cv2.line(frame, (200, 400), (360, 400), (0, 0, 255), 2)
    frame = cv2.line(frame, (200, 0), (200, 640), (0, 0, 255), 2)
    
    if x<160:
        curr_pos = "left"
    elif x>320:
        curr_pos = "right"
    elif y>400 and x>160 and x<320:
        curr_pos = "down"
    elif y<300 and x>160 and x<320:
        curr_pos = "up"
    else:
        curr_pos = "neutral"
        
    if curr_pos!=prev_pos:
        if curr_pos!="neutral":
            pyautogui.press(curr_pos)
        prev_pos = curr_pos
            
    
    cv2.imshow('DIP', frame)
    if cv2.waitKey(1)==ord('q'):
        break
    
vid.release()
cv2.destroyAllWindows()