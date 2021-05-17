from settings import *
from calculate import *
from graphics import *

if __name__=='__main__': 
    aStrengthy=[[0 for _ in range(HEIGHT)] for _ in range(WIDTH)]
    bStrengthy=[[0 for _ in range(HEIGHT)] for _ in range(WIDTH)]
    
    for xStart in range(0, WIDTH, START_SEPARATION):
        for yStart in range(0, HEIGHT, START_SEPARATION):
            for xIndex in range(xStart, xStart+START_WIDTH):
                for yIndex in range(yStart, yStart+START_WIDTH):
                    bStrengthy[xIndex][yIndex]=1
                    aStrengthy[xIndex][yIndex]=0

    Graphics.createVideo(aStrengthy, bStrengthy)