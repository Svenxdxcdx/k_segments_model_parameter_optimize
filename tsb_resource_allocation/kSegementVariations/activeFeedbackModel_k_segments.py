from tsb_resource_allocation.k_segments_model import KSegmentsModel

import matplotlib.pyplot as plt
import numpy as np
import os 
import datetime
from collections import Counter

BASE_MODLE_TRAININGS_K = 4

PERCENT_OF_RECALCULTE = 0.1

class ActiveFeedbackModel_k_segments(KSegmentsModel):
    
    
    _predictCounter = 0
    
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
        self.mode = "activeFeedbackModel" 
        self._memoryDataPoints = []
        self._recaluculateCounter = 0
        self._recaluculateMaxCounter = 0
        self._baseSegmenthLength = 0
        
    def calculate_k(self):
        memoryList = list(map(lambda d: (d[0]['_value']), self.files))
        self._memoryDataPoints = memoryList
        self.k = self.buildLookUpTable(memoryList)
        if self.k == 0:
            self.k = 1
        self.valid_k()
        pass
    
    
    
        
    # Numeric misstake get covered
    def buildLookUpTable(self, memoryList):
        memoryList.sort(key=len)
        smallestSize = len(memoryList[0])
        
        max_k = smallestSize
        
        biggestSize = len(memoryList[len(memoryList)-1])
        sizeDifference = biggestSize - smallestSize
        
        mostFrequntFileLen = self.calaclulateMostFrequentFileSize(memoryList)
        
        traingisSet = []
        for memory in memoryList:
            if len(memory) == mostFrequntFileLen:
                traingisSet.append(memory)
            if len(memory) > mostFrequntFileLen:
                break
        
        return self.memoryChangePoints(traingisSet)
        
    def memoryChangePoints(self, memoryValueTrainigsFile):
            
        sumUpK = 0
        
        for memoryArray in memoryValueTrainigsFile:
            
            sumUpK = sumUpK +  self.findChangePoints(memoryArray)
        
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
        return k + 1 
                
    def calaclulateMostFrequentFileSize(self, memoryList):
    
        memoryListLen = list(map(lambda d: len(d), memoryList))
        
        most_common_numbers = Counter(memoryListLen).most_common(1)
        return most_common_numbers[0][0]
        
    
    
    def recalculate(self):
        memoryValueTrainigsFile = list(self._memoryDataPoints)
        memoryValueTrainigsFile.sort(key=len)
        smallestMemoryLog = memoryValueTrainigsFile[0]
        segmentLength = int(len(smallestMemoryLog) / BASE_MODLE_TRAININGS_K)
       
        
        sumUpK = 0
        
        for memoryArray in memoryValueTrainigsFile:
            
            changePoint_k = self.findChangePoints(memoryArray)
            segment_k = int(len(memoryArray) / segmentLength)
            if changePoint_k > segment_k:
                sumUpK += changePoint_k
            else:
                sumUpK += segment_k
                
        #if self.k != int(sumUpK / len(memoryValueTrainigsFile)):
        #    print("New k: " + str(int(sumUpK / len(memoryValueTrainigsFile))))
        self.k = int(sumUpK / len(memoryValueTrainigsFile))
        
        self.valid_k()
        
    
    
    def evaluteData(self, data, currentFile):
        data_k = self.calculateData_k(data)
        self.mangeDataArray(data, currentFile)
        if data_k != self.k:
            
            self._recaluculateCounter += 1
        
        if self._recaluculateCounter >= self._recaluculateMaxCounter:
            self.recalculate()
            self._recaluculateCounter = 0
            pass
        pass
        
    
    def calculateData_k(self, data):
        return self.findChangePoints(data)
        
        
    def mangeDataArray(self, data, currentFile):
        self._memoryDataPoints.pop(0)
        self._memoryDataPoints.append(data)
        self.files.pop(0)
        self.files.append(currentFile)
        self.train_model()

    
    def valid_k(self):
        for y,_,x in self.files:
            if len(y) < self.k:
                self.k = len(y)