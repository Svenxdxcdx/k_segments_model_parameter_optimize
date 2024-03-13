import matplotlib.pyplot as plt
import seaborn as sns
import os
import math
import pandas as pd
import numpy as np

TWENTY_FIVE = 0
FIFTHY = 1
SEVENTHY_FIVE = 2
    

# Only for 4
def plotWastageBars(results):
    twentyFiveAverage, fifthyAverage, seventyFiveAverage = calculateAverageWaste(results)
    models = ["PeakMemory_k_segments", "FileEvents_k_segments", "KSegments retry: selective", "KSegments retry: partial"]
    
    df = pd.DataFrame({"25%": twentyFiveAverage,
                       "50%": fifthyAverage,
                       "75%": seventyFiveAverage}, index=models)
    ax = df.plot.bar(rot=0, color={"25%": "blue", "50%": "orange",  "75%": "green"})
    plt.show()
    pass

def plotWastageBarsDynamic(results, models):
    twentyFiveAverage, fifthyAverage, seventyFiveAverage = calculateAverageWaste(results)
    
    
    df = pd.DataFrame({"25%": twentyFiveAverage,
                       "50%": fifthyAverage,
                       "75%": seventyFiveAverage}, index=models)
    ax = df.plot.bar(rot=0, color={"25%": "blue", "50%": "orange",  "75%": "green"})
    for container in ax.containers:
        ax.bar_label(container)

# TODO
def safePlotWastageBarsDynamic(results, models):
    twentyFiveAverage, fifthyAverage, seventyFiveAverage = calculateAverageWaste(results)
    
    
    df = pd.DataFrame({"25%": twentyFiveAverage,
                       "50%": fifthyAverage,
                       "75%": seventyFiveAverage}, index=models)
    ax = df.plot.bar(rot=0, color={"25%": "blue", "50%": "orange",  "75%": "green"})
    for container in ax.containers:
        ax.bar_label(container)

def plotSelectedK_BarsDynamic(results, models):
    twentyFiveAverage, fifthyAverage, seventyFiveAverage = calculateAverageWaste(results)
    
    
    df = pd.DataFrame({"25%": twentyFiveAverage,
                       "50%": fifthyAverage,
                       "75%": seventyFiveAverage}, index=models)
    ax = df.plot.bar(rot=0, color={"25%": "blue", "50%": "orange",  "75%": "green"})
    for container in ax.containers:
        ax.bar_label(container)


def plotRuntimeBarsDynamic(results, models):
    twentyFiveAverage, fifthyAverage, seventyFiveAverage = calculateAverageWaste(results)
    
    
    df = pd.DataFrame({"25%": twentyFiveAverage,
                       "50%": fifthyAverage,
                       "75%": seventyFiveAverage}, index=models)
    ax = df.plot.bar(rot=0, color={"25%": "blue", "50%": "orange",  "75%": "green"})
    for container in ax.containers:
        ax.bar_label(container)




def plotRetriesBarsDynamic(results, models):
    twentyFiveAverage, fifthyAverage, seventyFiveAverage = calculateAverageWaste(results)
    
    
    df = pd.DataFrame({"25%": twentyFiveAverage,
                       "50%": fifthyAverage,
                       "75%": seventyFiveAverage}, index=models)
    ax = df.plot.bar(rot=0, color={"25%": "blue", "50%": "orange",  "75%": "green"})
    for container in ax.containers:
        ax.bar_label(container)

# @Param filePath has the name of the plot input
def safePlotsBarsDynamic(results, models, filePath):
    twentyFiveAverage, fifthyAverage, seventyFiveAverage = calculateAverageWaste(results)
    
    
    df = pd.DataFrame({"25%": twentyFiveAverage,
                       "50%": fifthyAverage,
                       "75%": seventyFiveAverage}, index=models)
    ax = df.plot.bar(rot=0, color={"25%": "blue", "50%": "orange",  "75%": "green"})
    for container in ax.containers:
        ax.bar_label(container)
    plt.gcf().set_size_inches(15, 5)
    plt.savefig(filePath + '.png', dpi=100)
    plt.close()



def calculateAverageWaste(results):
    twentyFive = []
    fifthy = []
    seventyFive = []
    
    addedFilesCounter = 0
    for i, result in enumerate(results):
        if len(result) != 3:
            print("One Left")
            continue
        if len(twentyFive) == 0:
            twentyFive = np.array(result[TWENTY_FIVE])
            fifthy = np.array(result[FIFTHY])
            seventyFive = np.array(result[SEVENTHY_FIVE])
            addedFilesCounter = addedFilesCounter + 1
            continue
        twentyFive = twentyFive + np.array(result[TWENTY_FIVE])
        fifthy = fifthy + np.array(result[FIFTHY])
        seventyFive = seventyFive + np.array(result[SEVENTHY_FIVE])
        addedFilesCounter = addedFilesCounter + 1
    
    twentyFiveAverage = twentyFive / addedFilesCounter
    fifthyAverage = fifthy / addedFilesCounter
    seventyFiveAverage = seventyFive / addedFilesCounter
    
    return twentyFiveAverage, fifthyAverage, seventyFiveAverage
    
