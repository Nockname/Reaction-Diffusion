from settings import *
from random import uniform, random, sample
import copy
import threading
import numpy as np

class Individual:
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
    def updatePixelStrength(aLevel, bLevel, xValue, yValue, ADIFFUSE, BDIFFUSE):

        newA=aLevel[xValue][yValue] + (
            Individual.__diffuse(aLevel, xValue, yValue) * ADIFFUSE 
            - aLevel[xValue][yValue] * bLevel[xValue][yValue] * bLevel[xValue][yValue]
            + FEEDRATE[xValue] * (1 - aLevel[xValue][yValue])
        ) * TIMESCALE

        newB=bLevel[xValue][yValue] + (
            Individual.__diffuse(bLevel, xValue, yValue) * BDIFFUSE 
            + aLevel[xValue][yValue] * bLevel[xValue][yValue] * bLevel[xValue][yValue]
            - bLevel[xValue][yValue] * (KILLRATE[yValue] + FEEDRATE[xValue])
        ) * TIMESCALE

        return newA, newB

    @staticmethod
    def processesUpdatePixelStrength(aLevel, bLevel, ADIFFUSE, BDIFFUSE, xStart, xEnd, endALevel, endBLevel):

        resultA=[[0 for _ in range(HEIGHT)] for _ in range(WIDTH)]
        resultB=[[0 for _ in range(HEIGHT)] for _ in range(WIDTH)]

        for xValue in range(xStart, xEnd):
            for yValue in range(HEIGHT):

                newA=aLevel[xValue][yValue] + (
                    Individual.__diffuse(aLevel, xValue, yValue) * ADIFFUSE 
                    - aLevel[xValue][yValue] * bLevel[xValue][yValue] * bLevel[xValue][yValue]
                    + FEEDRATE * (1 - aLevel[xValue][yValue])
                ) * TIMESCALE

                newB=bLevel[xValue][yValue] + (
                    Individual.__diffuse(bLevel, xValue, yValue) * BDIFFUSE 
                    + aLevel[xValue][yValue] * bLevel[xValue][yValue] * bLevel[xValue][yValue]
                    - bLevel[xValue][yValue] * (KILLRATE + FEEDRATE)
                ) * TIMESCALE

                resultA[xValue][yValue]=newA
                resultB[xValue][yValue]=newB

        endALevel[xStart:xEnd]=resultA[xStart:xEnd]
        endBLevel[xStart:xEnd]=resultB[xStart:xEnd]

class Calculate:

    @staticmethod
    def updateAllStrength(aLevel, bLevel):
        newALevel=[[0 for _ in range(HEIGHT)] for _ in range(WIDTH)]
        newBLevel=[[0 for _ in range(HEIGHT)] for _ in range(WIDTH)]
        for xValue in range(WIDTH):
            for yValue in range(HEIGHT):
                newALevel[xValue][yValue], newBLevel[xValue][yValue]=Individual.updatePixelStrength(
                    aLevel, bLevel, xValue, yValue, ADIFFUSE, BDIFFUSE)

        return newALevel, newBLevel

    @staticmethod
    def processesUpdateAllSrength(aLevel, bLevel):
        newALevel=[[0 for _ in range(HEIGHT)] for _ in range(WIDTH)]
        newBLevel=[[0 for _ in range(HEIGHT)] for _ in range(WIDTH)]

        widthStarts=np.linspace(0, WIDTH, N_PROCESSES, endpoint=False)
        processesRunning=[]

        for widthStart in widthStarts:
            process1 = threading.Thread(target=Individual.processesUpdatePixelStrength, args=(
                aLevel, bLevel, ADIFFUSE, BDIFFUSE, int(widthStart), 
                int(widthStart+WIDTH/N_PROCESSES), newALevel, newBLevel))

            processesRunning.append(process1)
            processesRunning[-1].start()
        
        for process1 in processesRunning:
            process1.join()

        return newALevel, newBLevel