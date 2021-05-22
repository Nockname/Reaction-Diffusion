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

        Red=int((COLORWHEEL[4]-COLORWHEEL[0])*aLevel+COLORWHEEL[0])
        Green=int((COLORWHEEL[5]-COLORWHEEL[1])*(aLevel+bLevel)/2+COLORWHEEL[1])
        Blue=int((COLORWHEEL[6]-COLORWHEEL[2])*bLevel+COLORWHEEL[2])

        return [Red, Green, Blue, 255]

    @staticmethod
    def __image(aStrength, bStrength, previousPixels, frame):

        print("Doing math")
        aStrength, bStrength=Calculate.updateAllStrength(aStrength, bStrength)

        pixels=previousPixels

        aSum=0
        bSum=0

        print("Doing graphics")
        for x in range(WIDTH):
            for y in range(HEIGHT):
                pixels[HEIGHT-y-1][x][0:4]=Graphics.__convert(aStrength[x][y], bStrength[x][y],
                CONVERT_METHOD, COLORWHEEL)[0:4]
                aSum+=aStrength[x][y]
                bSum+=bStrength[x][y]

        print("Saving Image")
        print("{} amount of A, {} amount of B, frame {}, {} percent done".format(aSum, bSum, frame, frame/FRAMES))
        image=Image.fromarray(np.uint8(pixels)).convert('RGB')
        image.save("./data/{}.png".format(frame))

        return aStrength, bStrength, pixels

    @staticmethod
    def createVideo(aStrength, bStrength): 

        pixels=np.ndarray( (HEIGHT, WIDTH, 4) )
        for frame in range(0, FRAMES):
            aStrength, bStrength, pixels=Graphics.__image(aStrength, bStrength, pixels, frame)

        if CREATE_VIDEO:
            os.system("ffmpeg -framerate {} -start_number 1 -i ./data/%d.png -vcodec libx264 -pix_fmt yuv420p {}.mov".format(FPS, VIDEO_NAME))
            os.system("open {}.mov".format(VIDEO_NAME))

        else:
            os.system("open ./data/{}.png".format(FRAMES-1))