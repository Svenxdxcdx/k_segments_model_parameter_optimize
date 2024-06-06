from tsb_resource_allocation.k_segments_model import KSegmentsModel

import matplotlib.pyplot as plt
import numpy as np
import os 
import datetime

BASE_MODLE_TRAININGS_K = 4

class MemoryAndSegmentLengthCombind_k_segments(KSegmentsModel):
    
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
        self.mode = "MemoryAndSegmentLengthCombind" # fileEvents, interploate
        
            
    def calculate_k(self):
        memoryValueTrainigsFile = list(map(lambda d: (d[0]['_value']), self.files))
        
        memoryValueTrainigsFile.sort(key=len)
        smallestMemoryLog = memoryValueTrainigsFile[0]
        segmentLength = self.findChangePoints(smallestMemoryLog)
        sumUpK = 0
        
        for memoryArray in memoryValueTrainigsFile:
            
            changePoint_k = self.findChangePoints(memoryArray)
            segment_k = int(len(memoryArray) / segmentLength)
            if changePoint_k > segment_k:
                sumUpK += changePoint_k
            else:
                sumUpK += segment_k
                
                
        self.k = int(sumUpK / len(memoryValueTrainigsFile))
        
        self.valid_k()
        pass
            
        
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
        return k + 1
                
    
    def valid_k(self):
        for y,_,x in self.files:
            if len(y) < self.k:
                self.k = len(y)