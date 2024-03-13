from tsb_resource_allocation.k_segments_model import KSegmentsModel

import matplotlib.pyplot as plt
import numpy as np
import os 
import datetime


BASE_MODLE_TRAININGS_K = 4

class SegmentLength_k_segments(KSegmentsModel):
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
        self.mode = "peakMemory" # fileEvents, interploate
        
    # memory is the first
    def calculate_k(self):
        memoryList = list(map(lambda d: (d[0]['_value']), self.files))
        memoryList.sort(key=len)
        smallestMemoryLog = memoryList[0]
        segmentLength = self.findChangePoints(smallestMemoryLog)
        numberOfAllSegments = 0
        for memoryLog in memoryList:
            numberOfSegments = int(len(memoryLog) / segmentLength)
            numberOfAllSegments += numberOfSegments
            
        self.k = int(numberOfAllSegments / len(memoryList))
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
        
        return k
                    

    
    def valid_k(self):
        for y,_,x in self.files:
            if len(y) < self.k:
                self.k = len(y)
        
