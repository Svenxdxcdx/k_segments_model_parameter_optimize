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


from plots.plotsBars import plotRuntimeBarsDynamic


from plots.plotsBars import safePlotsBarsDynamic
from plots.plotsBars import plotRetriesBarsDynamic


from plots.plotsBars import plotBestApporachAndk_sFirstProcent
#CURRENT_DIR = "eager"
#CURRENT_DIR = "sarek"
#CURRENT_DIR = "both"
#CURRENT_DIR = "bothDifferentKs"
#CURRENT_DIR = "eagerKs"
#CURRENT_DIR = "sarekKs"
#CURRENT_DIR = "rangeland"
#CURRENT_DIR = "third"
CURRENT_DIR = "thirdDifferentKs"
SAFE_FOLDER = "plotsPng\\" + CURRENT_DIR + "\\"

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
    fileNames = os.listdir("C:\\privat\\Bachelor_Work\\pytonProject\\k_segments_model_parameter_optimize\\pickleFiles\\" + CURRENT_DIR)
    
    dirPath = "pickleFiles\\" + CURRENT_DIR + "\\"
    fileType = ".pickle"

    
    wasteList = []
    k_list = []
    runtime_list = []
    retries_list = []
    nameList = []
    for fileName in fileNames:
        if "KSegmentsModel" not in fileName:
            expDict = readDictPickleFile(dirPath + fileName)
            
            wasteList.append(expDict["storageWaste"])
            
            
            k_list.append(expDict["k_selected"])
            runtime_list.append(expDict["runtime"])
            retries_list.append(expDict["retries"])
            
            nameList.append(expDict["models"])
        
    cutFileNames = list(map(lambda x: (x.split(".")[0]), fileNames))
    
            
    for waste, k, name, fileName in zip(wasteList, k_list, nameList, cutFileNames):
        #plotWastageBarsDynamic(waste, name)
        #plotSelectedK_BarsDynamic(k, name)
        pass
        
    for runtime, retries, name, fileName in zip(runtime_list, retries_list, nameList, cutFileNames):
        
        
        #plotRuntimeBarsDynamic(runtime, name)
        #plotRetriesBarsDynamic(retries, name)
        pass
    
        
    plt.show()
        
        
#safePlotsBarsDynamic(runtime, name, SAFE_FOLDER + fileName)

def readAndSafeAllPlotFileNames():
    fileNames = os.listdir("C:\\privat\\Bachelor_Work\\pytonProject\\k_segments_model_parameter_optimize\\pickleFiles\\" + CURRENT_DIR)
    
    dirPath = "pickleFiles\\" + CURRENT_DIR + "\\"
    fileType = ".pickle"

    
    wasteList = []
    k_list = []
    runtime_list = []
    retries_list = []
    nameList = []
    for fileName in fileNames:
        if "KSegmentsModel" not in fileName:
            expDict = readDictPickleFile(dirPath + fileName)
            
            wasteList.append(expDict["storageWaste"])
            
            
            k_list.append(expDict["k_selected"])
            runtime_list.append(expDict["runtime"])
            retries_list.append(expDict["retries"])
            
            nameList.append(expDict["models"])
        
    cutFileNames = list(map(lambda x: (x.split(".")[0]), fileNames))
    
            
    for waste, k, name, fileName in zip(wasteList, k_list, nameList, cutFileNames):
        safePlotsBarsDynamic(waste, name, SAFE_FOLDER + fileName + "_storage_waste")
        safePlotsBarsDynamic(k, name, SAFE_FOLDER + fileName + "k_Bars")
        #plotWastageBarsDynamic(waste, name)
        #plotSelectedK_BarsDynamic(k, name)
        pass
        
    for runtime, retries, name, fileName in zip(runtime_list, retries_list, nameList, cutFileNames):
        #safePlotRuntimeBarsDynamic(runtime, name, SAFE_FOLDER + fileName)
        safePlotsBarsDynamic(runtime, name, SAFE_FOLDER + fileName + "runtime")
        safePlotsBarsDynamic(retries, name, SAFE_FOLDER + fileName + "retries")
        #plotRuntimeBarsDynamic(runtime, name)
        #plotRetriesBarsDynamic(retries, name)
        pass
    
    
def readAndSafeAllPlotFileNamesAdaptForError():
    fileNames = os.listdir("C:\\privat\\Bachelor_Work\\pytonProject\\k_segments_model_parameter_optimize\\pickleFiles\\" + CURRENT_DIR)
    
    dirPath = "pickleFiles\\" + CURRENT_DIR + "\\"
    fileType = ".pickle"

    
    wasteList = []
    k_list = []
    runtime_list = []
    retries_list = []
    nameList = []
    for fileName in fileNames:
        if "KSegmentsModel" not in fileName:
            expDict = readDictPickleFile(dirPath + fileName)
            
            wasteList.append(expDict["storageWaste"])
            
            
            k_list.append(expDict["k_selected"])
            runtime_list.append(expDict["runtime"])
            retries_list.append(expDict["retries"])
            
            nameList.append(expDict["models"])
        
    cutFileNames = list(map(lambda x: (x.split(".")[0]), fileNames))
    
            
    for waste, k, name, fileName in zip(wasteList, k_list, nameList, cutFileNames):
        
        safePlotsBarsDynamic(waste, name, SAFE_FOLDER + fileName + "_storage_waste")
        safePlotsBarsDynamic(k, name, SAFE_FOLDER + fileName + "k_Bars")
        #plotWastageBarsDynamic(waste, name)
        #plotSelectedK_BarsDynamic(k, name)
        pass
        
    for runtime, retries, name, fileName in zip(runtime_list, retries_list, nameList, cutFileNames):
        #safePlotRuntimeBarsDynamic(runtime, name, SAFE_FOLDER + fileName)
        safePlotsBarsDynamic(runtime, name, SAFE_FOLDER + fileName + "runtime")
        safePlotsBarsDynamic(retries, name, SAFE_FOLDER + fileName + "retries")
        #plotRuntimeBarsDynamic(runtime, name)
        #plotRetriesBarsDynamic(retries, name)
        pass
    

def plotOneFile():
    fileNames = ["AverageMemory_k.pickle"]
    
    dirPath = "pickleFiles\\" + CURRENT_DIR + "\\"
    fileType = ".pickle"

    
    wasteList = []
    k_list = []
    runtime_list = []
    retries_list = []
    nameList = []
    for fileName in fileNames:
        if "KSegmentsModel" not in fileName:
            expDict = readDictPickleFile(dirPath + fileName)
            
            wasteList.append(expDict["storageWaste"])
            
            
            k_list.append(expDict["k_selected"])
            runtime_list.append(expDict["runtime"])
            retries_list.append(expDict["retries"])
            
            nameList.append(expDict["models"])
        
    cutFileNames = list(map(lambda x: (x.split(".")[0]), fileNames))
    
            
    for waste, k, name, fileName in zip(wasteList, k_list, nameList, cutFileNames):
        safePlotsBarsDynamic(waste, name, SAFE_FOLDER + fileName + "_storage_waste")
        safePlotsBarsDynamic(k, name, SAFE_FOLDER + fileName + "k_Bars")
        #plotWastageBarsDynamic(waste, name)
        #plotSelectedK_BarsDynamic(k, name)
        pass
        
    for runtime, retries, name, fileName in zip(runtime_list, retries_list, nameList, cutFileNames):
        #safePlotRuntimeBarsDynamic(runtime, name, SAFE_FOLDER + fileName)
        safePlotsBarsDynamic(runtime, name, SAFE_FOLDER + fileName + "runtime")
        safePlotsBarsDynamic(retries, name, SAFE_FOLDER + fileName + "retries")
        #plotRuntimeBarsDynamic(runtime, name)
        #plotRetriesBarsDynamic(retries, name)
        pass
    pass

def plotKsSortedAndBestApproach():
    fileNames = os.listdir("C:\\privat\\Bachelor_Work\\pytonProject\\k_segments_model_parameter_optimize\\pickleFiles\\" + "thirdDifferentKs")
    bestAppraochPath = "C:\\privat\\Bachelor_Work\\pytonProject\\k_segments_model_parameter_optimize\\pickleFiles\\third\\SameFileSizeMCP_k.pickle"
    dirPath = "pickleFiles\\" + "thirdDifferentKs" + "\\"
    fileType = ".pickle"

    
    wasteList = []
    k_list = []
    runtime_list = []
    retries_list = []
    nameList = []
    for fileName in fileNames:
        if "KSegmentsModel" not in fileName:
            expDict = readDictPickleFile(dirPath + fileName)
            
            wasteList.append(expDict["storageWaste"])
            
            
            k_list.append(expDict["k_selected"])
            runtime_list.append(expDict["runtime"])
            retries_list.append(expDict["retries"])
            
            nameList.append(str(expDict["k_selected"][0][0][0]))
        
    
    bestAppraochDict = readDictPickleFile(bestAppraochPath)
    cutFileNames = list(map(lambda x: (x.split(".")[0]), fileNames))
    plotBestApporachAndk_sFirstProcent(bestAppraochDict, wasteList, nameList)

    pass
if __name__ == "__main__":
    #results = readPickleFile()
    #plotWastageBars(results)
    #plotAllModelsWasteHandler()
    #plotSelectedK_handler()
    #readAllFIleNames()
    #readAndSafeAllPlotFileNames()
    #readAndSafeAllPlotFileNamesAdaptForError()
    #plotOneFile()
    #plt.show()
    plotKsSortedAndBestApproach()



