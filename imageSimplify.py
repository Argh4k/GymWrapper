from gym import envs
import gym
import cv2
import numpy as np
import math

kernel = np.ones((2,2),np.uint8)


def simplifyAtariOutput(observation):
    intermediate = cv2.cvtColor(observation, cv2.COLOR_RGB2HSV)
    sat = intermediate[:,:,1]
    sat = cv2.dilate(sat, kernel, iterations = 1)

    filtered = cv2.Canny(sat, 100, 50, 2)
    filtered = cv2.morphologyEx(filtered, cv2.MORPH_CLOSE, kernel)
    im2, contours, hierarchy = cv2.findContours(filtered,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

    knownCountours = []
    newCountours = []

    for cnt in contours:
        permitere = cv2.arcLength(cnt, True)
        area = cv2.contourArea(cnt)
        if permitere > 5 and area > 10:
            newCountours.append(cnt)

    tiles = [0] * (16*21)

    for cnt in newCountours:
        isOk = False
        M = cv2.moments(cnt)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        tileX = cX // 10
        tileY = cY // 10
        index = 0
        matched = False
        for kcnt in knownCountours:
            if cv2.matchShapes(cnt, kcnt, 1,0.0) < 0.05:
                tiles[tileY*16 + tileX] = index + 1
                matched=True
            index = index+1    
        if matched == False:
            knownCountours.append(cnt)
            tiles[tileY*16 + tileX] = len(knownCountours)
    return tiles
