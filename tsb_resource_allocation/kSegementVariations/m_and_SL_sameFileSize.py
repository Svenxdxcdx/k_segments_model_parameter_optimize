from tsb_resource_allocation.k_segments_model import KSegmentsModel
from statistics import multimode
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import os 
import datetime
import math
"""_summary_
The retry model increases the k with a look up table. The look up table is based with different k, for example low, mid and high.
The selection is based on the procent parts of file size. For example if mainly small size files exists, the modle take from the look 
up table a k form from the low part. 

range 
"""

NUMBER_OF_PARTS = 10
START_K = 4

class M_and_SL_sameFileSize(KSegmentsModel):
    
    def __init__(
            self,
            monotonically_increasing = True,
            default_value = 100,
            k = 2,
            time_mode = 1,
        ):
        super().__init__(
            monotonically_increasing,
            default_value,
            k,
            time_mode)
        self.mode = "lookUpTable" # fileEvents, interploate#
        
    def calculate_k(self):
        memoryList = list(map(lambda d: (d[0]['_value']), self.files))
        self.k = self.buildLookUpTable(memoryList)
        if self.k == 0:
            self.k = 1
        self.valid_k()
        pass
    
    
    
        
    # Numeric misstake get covered
    def buildLookUpTable(self, memoryList):
        memoryList.sort(key=len)
        
        memoryList.sort(key=len)
        smallestMemoryLog = memoryList[0]
        segmentLength = self.findChangePoints(smallestMemoryLog)
        mostFrequntFileLen = self.calaclulateMostFrequentFileSize(memoryList)
        
        traingisSet = []
        for memory in memoryList:
            if len(memory) == mostFrequntFileLen:
                traingisSet.append(memory)
            if len(memory) > mostFrequntFileLen:
                break
        
        return self.memoryChangePoints(traingisSet, segmentLength)
        
        
    def memoryChangePoints(self, memoryValueTrainigsFile, segmentLength):
            
        sumUpK = 0
        
        for memoryArray in memoryValueTrainigsFile:
            
            changePoint_k = self.findChangePoints(memoryArray)
            segment_k = int(len(memoryArray) / segmentLength)
            if changePoint_k > segment_k:
                sumUpK += changePoint_k
            else:
                sumUpK += segment_k
        
        return int(sumUpK / len(memoryValueTrainigsFile))
        
        
    def findChangePoints(self, memoryArray):
        avaerage = np.average(memoryArray)
        k = 0
        currentLow = True
        currentHigh = True
        for memoryLogSample in memoryArray:
            if memoryLogSample <= avaerage and currentHigh:
                k += 1
                currentLow = True
                currentHigh = False
            if memoryLogSample > avaerage and currentLow:
                k += 1
                currentHigh = True
                currentLow = False
        if (k == 0):
            pass
        return k
                
    def calaclulateMostFrequentFileSize(self, memoryList):
    
        memoryListLen = list(map(lambda d: len(d), memoryList))
        
        most_common_numbers = Counter(memoryListLen).most_common(1)
        return most_common_numbers[0][0]
        
    
        
        
    
    def selectLookUpTablePart(self, smallestSize, strongestFileSizeIndex, numberOfParts):
        return int((smallestSize / numberOfParts) + (strongestFileSizeIndex))
    
    def valid_k(self):
        for y,_,x in self.files:
            if len(y) < self.k:
                self.k = len(y)
        
    def selectK(self):
        pass