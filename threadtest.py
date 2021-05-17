import threading
import numpy as np

N_PROCESSES=1

list1=[i for i in range(1, 10000000)]
list2=[i for i in range(2, 10000001)]

def addTwo(listA, listB, startIndex, endIndex, endGoal):

    for i in range(int(startIndex), int(endIndex)):
        endGoal[i]=listA[i]+listB[i]

def doProcess():
    widthStarts=np.linspace(0, len(list1), N_PROCESSES, endpoint=False)
    processesRunning=[]
    answer=[0 for _ in range(len(list1))]

    for widthStart in widthStarts:
        processesRunning.append(threading.Thread(target=addTwo, args=(
            list1, list2, int(widthStart), int(widthStart+len(list1)/N_PROCESSES), answer)))

        processesRunning[-1].start()
    
    for process1 in processesRunning:
        process1.join()

doProcess()
