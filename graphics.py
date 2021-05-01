from settings import *
from calculate import *
import os
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from random import randint

from math import log

class Graphics:
    @staticmethod
    def __convert(aLevel, bLevel, CONVERT_METHOD, COLORWHEEL):
        if CONVERT_METHOD=="linear":
            aMagnitudePercent = aLevel
            bMagnitudePercent = bLevel
        elif CONVERT_METHOD=="expontial":
            aMagnitudePercent=10**(aLevel-1)
            bMagnitudePercent=10**(bLevel-1)

        magnitudePercent=(aMagnitudePercent+bMagnitudePercent)/2
        
        Red=int((COLORWHEEL[4]-COLORWHEEL[0])*aMagnitudePercent+COLORWHEEL[0])
        Green=int((COLORWHEEL[5]-COLORWHEEL[1])*magnitudePercent+COLORWHEEL[1])
        Blue=int((COLORWHEEL[6]-COLORWHEEL[2])*bMagnitudePercent+COLORWHEEL[2])
        Alpha=int((COLORWHEEL[7]-COLORWHEEL[3])*magnitudePercent+COLORWHEEL[3])

        return [Red, Green, Blue, Alpha]

    @staticmethod
    def __image(aStrength, bStrength, frame):

        if DO_PROCESSES and __name__=='__main__':
            print("PROCESSES UP AND RUNNING")
            aStrength, bStrength=Calculate.processesUpdateAllSrength(aStrength, bStrength)
        else:
            print("PROCESSES NOT WORKING")
            aStrength, bStrength=Calculate.updateAllStrength(aStrength, bStrength)

        print("CALC CODE DONE")

        pixels=np.ndarray( (WIDTH, HEIGHT, 4) )

        aSum=0
        bSum=0

        for x in range(WIDTH):
            for y in range(HEIGHT):
                pixels[x][y][0:4]=Graphics.__convert(aStrength[x][y], bStrength[x][y],
                CONVERT_METHOD, COLORWHEEL)[0:4]
                aSum+=aStrength[x][y]
                bSum+=bStrength[x][y]


        print(aSum, bSum, frame, frame/FRAMES)
        image=Image.fromarray(np.uint8(pixels)).convert('RGB')
        image.save("./data/{}.png".format(frame))


        # FEEDRATE=0.0567
        # KILLRATE=0.0449

        # KILLRATE+=0.001
        # FEEDRATE-=0.0005

        # for _ in range(TIMESCALE*10):
        #     aStrength[randint(0, WIDTH-1)][randint(0, HEIGHT-1)]=1
        #     bStrength[randint(0, WIDTH-1)][randint(0, HEIGHT-1)]=1

        return aStrength, bStrength

    @staticmethod
    def createVideo(aStrength, bStrength): 
        for frame in range(0, FRAMES):
            aStrength, bStrength=Graphics.__image(aStrength, bStrength, frame)
            
        os.system("ffmpeg -framerate {} -start_number 1 -i ./data/%d.png {}.mov".format(FPS, VIDEO_NAME))
    
Graphics.createVideo(aStrength, bStrength)