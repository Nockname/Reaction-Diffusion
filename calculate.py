from settings import *
from random import uniform, random, sample
import copy
import threading
import numpy as np

class Calculate:
    @staticmethod
    def __diffuse(strength, xValue, yValue):

        count=[0, 0]
        for xTest in range(xValue-1, xValue+2, 2):
            for yTest in range(yValue-1, yValue+2, 2):
                if xTest<WIDTH and xTest>0 and yTest<HEIGHT and yTest>0:
                    count[0]+=strength[xTest][yTest]*0.05
                    count[1]+=0.05
        
        for xTest in range(xValue-1, xValue+2, 2):
            if xTest<WIDTH and xTest>0:
                    count[0]+=strength[xTest][yValue]*0.2
                    count[1]+=0.2
        
        for yTest in range(yValue-1, yValue+2, 2):
                if yTest<HEIGHT and yTest>0:
                    count[0]+=strength[xValue][yTest]*0.2
                    count[1]+=0.2

        return (strength[xValue][yValue]*(-count[1])+count[0])

    @staticmethod
    def __updatePixelStrength(aLevel, bLevel, xValue, yValue, ADIFFUSE, BDIFFUSE):

        newA=aLevel[xValue][yValue] + (
            Calculate.__diffuse(aLevel, xValue, yValue) * ADIFFUSE 
            - aLevel[xValue][yValue] * bLevel[xValue][yValue] * bLevel[xValue][yValue]
            + FEEDRATE[xValue] * (1 - aLevel[xValue][yValue])
        ) * TIMESCALE

        newB=bLevel[xValue][yValue] + (
            Calculate.__diffuse(bLevel, xValue, yValue) * BDIFFUSE 
            + aLevel[xValue][yValue] * bLevel[xValue][yValue] * bLevel[xValue][yValue]
            - bLevel[xValue][yValue] * (KILLRATE[yValue] + FEEDRATE[xValue])
        ) * TIMESCALE

        return newA, newB

    @staticmethod
    def updateAllStrength(aLevel, bLevel):
        newALevel=[[0 for _ in range(HEIGHT)] for _ in range(WIDTH)]
        newBLevel=[[0 for _ in range(HEIGHT)] for _ in range(WIDTH)]
        for xValue in range(WIDTH):
            for yValue in range(HEIGHT):
                newALevel[xValue][yValue], newBLevel[xValue][yValue]=Calculate.__updatePixelStrength(
                    aLevel, bLevel, xValue, yValue, ADIFFUSE, BDIFFUSE)

        return newALevel, newBLevel