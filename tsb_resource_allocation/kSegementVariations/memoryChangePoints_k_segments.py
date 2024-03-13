from tsb_resource_allocation.k_segments_model import KSegmentsModel

import matplotlib.pyplot as plt
import numpy as np
import os 
import datetime
"""
The retry model gets a k based on the avearge file size divide by 4. (If the avagere file will be bigger then 4)
"""
class MemoryChangePoints_k_segments(KSegmentsModel):
    
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
        self.mode = "fileSize" # fileEvents, interploate
        
    def calculate_k(self):
        memoryValueTrainigsFile = []
        memoryValueTrainigsFile = list(map(lambda d: (d[0]['_value']), self.files))
            
        sumUpK = 0
        
        for memoryArray in memoryValueTrainigsFile:
            
            sumUpK = sumUpK +  self.findChangePoints(memoryArray)
        
        self.k = int(sumUpK / len(memoryValueTrainigsFile))
        
        self.valid_k(memoryValueTrainigsFile)
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
        if (k == 0):
            pass
        return k
                
    # divide to the 
    
    
    def valid_k(self, memoryValueTrainigsFile):
        
        for memory in memoryValueTrainigsFile:
            if len(memory) < self.k:
                self.k = len(memory)
            if self.k == 0:
                pass