import matplotlib.pyplot as plt
import seaborn as sns
import os
import math
import pandas as pd
import numpy as np
import statistics

DIR = "plotsPng\\approachGraphs"

BASE_X = [0,1,2,3,4,5,6,7,8,9]

BASE_Y = [0,1,3,2,1,2,3,4,2,0]



def plotFirst():
    plt.plot(BASE_X,BASE_Y)
    
    plt.xlabel("Time in Seconds")
    plt.ylabel("Memory Usage")
    
    plt.show()
    

def plotMemoryChnagePoint():
    plt.plot(BASE_X,BASE_Y, color='blue', marker = 'o', label = "Memory Usage")
    
    plt.xlabel("Time in Seconds")
    plt.ylabel("Memory in Gigabytes ")
    mean = np.mean(BASE_Y)
    meanLine = np.zeros(10)
    for index in range(10):
        meanLine[index] = mean
    plt.plot(BASE_X,meanLine, color='green', label = "Change Line")
    plt.legend(loc='upper center')
    plt.savefig(DIR+ '\\changePoint.png')
    
def plotSegemtPartsLength():
    plt.plot(BASE_X,BASE_Y, color='blue', marker = 'o', label = "Memory Usage")
    
    plt.xlabel("Time in Seconds")
    plt.ylabel("Memory in Gigabytes ")
    segementParts_X = [0,1]
    segementParts_Y = [0,0]
    
    plt.plot(segementParts_X,segementParts_Y, color='red', label = "One SegmentPart")
    plt.legend(loc='upper center')
    plt.savefig(DIR+ '\\segments.png')
    
    
def plotPeakMemory():
    plt.plot(BASE_X,BASE_Y, color='blue', marker = 'o', label = "Memory Usage")
    
    plt.xlabel("Time in Seconds")
    plt.ylabel("Memory in Gigabytes ")
    
    segementParts_X = [2,7]
    segementParts_Y = [3,4]
    
    plt.plot(segementParts_X,segementParts_Y, 'x',color='red', label = "Peaks")
    
    
    plt.legend(loc='upper center')
    plt.savefig(DIR+ '\\peakMemory.png')
    
    
    
def plotLimitations():
    limit_Y = [0,1,1,1,1,3,9,4,9,0]
    plt.plot(BASE_X,limit_Y, color='blue', marker = 'o', label = "Memory Usage")
    
    plt.xlabel("Time in Seconds")
    plt.ylabel("Memory in Gigabytes ")
    mean = np.mean(limit_Y)
    meanLine = np.zeros(10)
    for index in range(10):
        meanLine[index] = mean
    plt.plot(BASE_X,meanLine, color='green', label = "Change Line")
    plt.legend(loc='upper center')
    plt.show()
    plt.savefig(DIR+ '\\limit.png')
    
    
if __name__ == "__main__":
    #plotMemoryChnagePoint()
    #plotSegemtPartsLength()
    plotPeakMemory()
    #plotLimitations()
