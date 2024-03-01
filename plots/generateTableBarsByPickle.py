import pickle
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import os
import math
import pandas as pd

PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(
    PROJECT_PATH
)
sys.path.append(SOURCE_PATH)

from plots.plotsBars import plotWastageBars
from plots.plotsBars import plotWastageBarsDynamic

from plots.plotsBars import plotSelectedK_BarsDynamic


def readPickleFile():
    filePath = "wasteResults.pickle"
    with open(filePath, 'rb') as f:
        results = pickle.load(f)
    return results
    
def readDictPickleFile(filePath):
    with open(filePath, 'rb') as f:
        resultDict = pickle.load(f)
    return resultDict


def plotAllModelsWasteHandler():
    resultDict = readDictPickleFile("updateDirs.pickle")
    
    plotWastageBarsDynamic(resultDict["storageWaste"], resultDict["models"])

 
def plotSelectedK_handler():
    resultDict = readDictPickleFile("newModlesResults.pickle")
    plotSelectedK_BarsDynamic(resultDict["k_selected"], resultDict["models"])
    

if __name__ == "__main__":
    #results = readPickleFile()
    #plotWastageBars(results)
    plotAllModelsWasteHandler()
    #plotSelectedK_handler()
    plt.show()



