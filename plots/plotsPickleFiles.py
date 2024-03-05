import pickle
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import os
import math
import pandas as pd
from os import listdir
from os.path import isfile, join

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
    resultDict = readDictPickleFile("pickleFiles\\PeakMemory_k_segments_selective.pickle")
    
    plotWastageBarsDynamic(resultDict["storageWaste"], resultDict["models"])

 
def plotSelectedK_handler():
    resultDict = readDictPickleFile("newModlesResults.pickle")
    plotSelectedK_BarsDynamic(resultDict["k_selected"], resultDict["models"])
    
def readAllFIleNames():
    fileNames = os.listdir("C:\\privat\\Bachelor_Work\\pytonProject\\k_segments_model_parameter_optimize\\pickleFiles")
    
    dirPath = "pickleFiles\\"
    fileType = ".pickle"

    
    wasteList = []
    k_list = []
    nameList = []
    for fileName in fileNames:
        if "KSegmentsModel" not in fileName:
            expDict = readDictPickleFile(dirPath + fileName)
            
            wasteList.append(expDict["storageWaste"])
            
            
            k_list.append(expDict["k_selected"])
        
            
            nameList.append(expDict["models"])
        
            
            
    for waste, k, name in zip(wasteList, k_list, nameList):
        plotWastageBarsDynamic(waste, name)
       # plotSelectedK_BarsDynamic(k, name)
        
    plt.show()
        
if __name__ == "__main__":
    #results = readPickleFile()
    #plotWastageBars(results)
    #plotAllModelsWasteHandler()
    #plotSelectedK_handler()
    readAllFIleNames()
    plt.show()



