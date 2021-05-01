from random import sample, shuffle, uniform, random
from math import pi
import numpy as np

WIDTH=500
HEIGHT=500
TIMESCALE=1

DO_FEED_KILL_LIST=True
if DO_FEED_KILL_LIST:
    FEEDRATE=np.linspace(0.01, 0.1, WIDTH, endpoint=True)
    KILLRATE=np.linspace(0.01, 0.1, HEIGHT, endpoint=True)
else:
    FEEDRATE=0.02
    KILLRATE=0.03

CONVERT_METHOD="linear"
MIN_COLOR=[0, 0, 0, 255]
MAX_COLOR=[255, 255, 255, 255]

ADIFFUSE=1
BDIFFUSE=0.5

DO_PROCESSES=False
N_PROCESSES=8

COLORWHEEL=MAX_COLOR+MIN_COLOR

aStrength=[[0 for _ in range(HEIGHT)] for _ in range(WIDTH)]
bStrength=[[0 for _ in range(HEIGHT)] for _ in range(WIDTH)]
for xIndex in range(38, 44):
    for yIndex in range(13, 18):
        bStrength[xIndex][yIndex]=1
        aStrength[xIndex][yIndex]=0

"""startingInfectedList=[0]*N_HUMANS
for i in range(STARTINGINFECTED):
    startingInfectedList[i]=INFECTIONTIME
shuffle(startingInfectedList)

infection=[[-1 for _ in range(HEIGHT)] for _ in range(WIDTH)]
direction=[[False for _ in range(HEIGHT)] for _ in range(WIDTH)]
counter=0
for pos in sample(range(WIDTH*HEIGHT), N_HUMANS):
    infection[pos%WIDTH][pos//WIDTH] = startingInfectedList[counter]
    # direction[pos%WIDTH][pos//WIDTH] = np.random.random()*2*pi
    direction[pos%WIDTH][pos//WIDTH] =sample([0, pi/4, pi/2, 3*pi/4, pi, 5*pi/4, 3*pi/2, 7*pi/4], 1)[0]
    counter+=1"""

FRAMES=3000
FPS=60
VIDEO_NAME="diffusion"