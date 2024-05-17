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
def safePlotsBarsDynamic(results, models, filePath, yAxisLabel = None):
    twentyFiveAverage, fifthyAverage, seventyFiveAverage = calculateAverageWaste(results)
    
    
    df = pd.DataFrame({"25%": twentyFiveAverage,
                       "50%": fifthyAverage,
                       "75%": seventyFiveAverage}, index=models)
    ax = df.plot.bar(rot=0, color={"25%": "blue", "50%": "orange",  "75%": "green"})
    if yAxisLabel != None:
        ax.set_ylabel(yAxisLabel)
    for container in ax.containers:
        ax.bar_label(container)
    plt.gcf().set_size_inches(20, 5)
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
    


def plotBestApporachAndk_sFirstProcent(bestApproachDict, resultsList, modelsList):
    resultsDictList = []
    for results,model in zip(resultsList, modelsList):
        # 0 selective
        # 1 partial
        twentyFiveAverage, fifthyAverage, seventyFiveAverage = calculateAverageWaste(results)
        modelsDict = {
            "25s": twentyFiveAverage[0],
            "50s": fifthyAverage[0],
            "75s": seventyFiveAverage[0],
            "25p": twentyFiveAverage[1],
            "50p": fifthyAverage[1],
            "75p": seventyFiveAverage[1],
            "name": model
        }
        resultsDictList.append(modelsDict)
    bestTwenty, bestFifthy, bestSeventy = calculateAverageWaste(bestApproachDict["storageWaste"])
    bestModelsDict = {
            "25s": bestTwenty[0],
            "50s": bestFifthy[0],
            "75s": bestSeventy[0],
            "25p": bestTwenty[1],
            "50p": bestFifthy[1],
            "75p": bestSeventy[1],
            "name": "Appraoch"
        }
    resultsDictList.append(bestModelsDict)
    
    sorted25s = sorted(resultsDictList, key=lambda x: x["25s"])
    plotDictselective(sorted25s, "25% StorageWaste Selective", "25")
    
    sorted50s = sorted(resultsDictList, key=lambda x: x["50s"])
    plotDictselective(sorted50s, "50% StorageWaste Selective", "50")
    
    sorted75s = sorted(resultsDictList, key=lambda x: x["75s"])
    plotDictselective(sorted75s, "75% StorageWaste Selective", "75")
    
    
    
    sorted25p = sorted(resultsDictList, key=lambda x: x["25p"])
    plotDictpartiell(sorted25p, "25% StorageWaste Partial", "25")
    
    sorted50p = sorted(resultsDictList, key=lambda x: x["50p"])
    plotDictpartiell(sorted50p, "50% StorageWaste Partial", "50")
    
    sorted75p = sorted(resultsDictList, key=lambda x: x["75p"])
    plotDictpartiell(sorted75p, "75% StorageWaste Partial", "75")
    
    
    
    
#    
def plotDictselective(resultsDictList, title, proecent):
    models = list(map(lambda x: (x["name"]), resultsDictList))
    results = list(map(lambda x: (x[proecent + "s"]), resultsDictList))
    df = pd.DataFrame({proecent + "%": results}, index=models)
    #ax = df.plot.bar(rot=0, color={"25%": "blue", "50%": "orange",  "75%": "green"})
    if proecent == "25":
        ax = df.plot.bar(rot=0, color={"25%": "blue"})
    if proecent == "50":
        ax = df.plot.bar(rot=0, color={"50%": "orange"})
    if proecent == "75":
        ax = df.plot.bar(rot=0, color={"75%": "green"})
    for container in ax.containers:
        ax.bar_label(container)
    ax.set_title(title)
    ax.set_ylabel("Average Wastage (Gigabyte-Seconds)")
    plt.gcf().set_size_inches(15, 5)
    #plt.show()
    pathPng = "plotsPng\\sortedPlots\\" + proecent +"s.png"
    plt.savefig(pathPng, dpi=100)
    plt.close()

def plotDictpartiell(resultsDictList, title, proecent):
    models = list(map(lambda x: (x["name"]), resultsDictList))
    results = list(map(lambda x: (x[proecent + "p"]), resultsDictList))
    df = pd.DataFrame({proecent + "%": results}, index=models)
    #ax = df.plot.bar(rot=0, color={"25%": "blue", "50%": "orange",  "75%": "green"})
    if proecent == "25":
        ax = df.plot.bar(rot=0, color={"25%": "blue"})
    if proecent == "50":
        ax = df.plot.bar(rot=0, color={"50%": "orange"})
    if proecent == "75":
        ax = df.plot.bar(rot=0, color={"75%": "green"})
    for container in ax.containers:
        ax.bar_label(container)
    ax.set_title(title)
    ax.set_ylabel("Average Wastage (Gigabyte-Seconds)")
    plt.gcf().set_size_inches(15, 5)
    #plt.show()
    pathPng = "plotsPng\\sortedPlots\\" + proecent +"p.png"
    plt.savefig(pathPng, dpi=100)
    plt.close()
    
