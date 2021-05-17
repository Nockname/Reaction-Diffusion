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

        try:
            Red=int((COLORWHEEL[4]-COLORWHEEL[0])*aMagnitudePercent+COLORWHEEL[0])
            Green=int((COLORWHEEL[5]-COLORWHEEL[1])*magnitudePercent+COLORWHEEL[1])
            Blue=int((COLORWHEEL[6]-COLORWHEEL[2])*bMagnitudePercent+COLORWHEEL[2])
            Alpha=int((COLORWHEEL[7]-COLORWHEEL[3])*magnitudePercent+COLORWHEEL[3])
        except:
            print(aMagnitudePercent)

        return [Red, Green, Blue, Alpha]

    @staticmethod
    def __image(aStrength, bStrength, frame):

        aStrength, bStrength=Calculate.updateAllStrength(aStrength, bStrength)

        pixels=np.ndarray( (HEIGHT, WIDTH, 4) )

        aSum=0
        bSum=0

        for x in range(WIDTH):
            for y in range(HEIGHT):
                pixels[HEIGHT-y-1][x][0:4]=Graphics.__convert(aStrength[x][y], bStrength[x][y],
                CONVERT_METHOD, COLORWHEEL)[0:4]
                aSum+=aStrength[x][y]
                bSum+=bStrength[x][y]


        print("{} amount of A, {} amount of B, frame {}, {} percent done".format(aSum, bSum, frame, frame/FRAMES))
        image=Image.fromarray(np.uint8(pixels)).convert('RGB')
        image.save("./data/{}.png".format(frame))

        return aStrength, bStrength

    @staticmethod
    def createVideo(aStrength, bStrength): 
        for frame in range(0, FRAMES):
            aStrength, bStrength=Graphics.__image(aStrength, bStrength, frame)

        if CREATE_VIDEO:
            os.system("ffmpeg -framerate {} -start_number 1 -i ./data/%d.png -vcodec libx264 -pix_fmt yuv420p {}.mov".format(FPS, VIDEO_NAME))
            os.system("open {}.mov".format(VIDEO_NAME))

        else:
            os.system("open ./data/{}.png".format(FRAMES-1))