from tsb_resource_allocation.k_segments_model import KSegmentsModel

import matplotlib.pyplot as plt
import numpy as np
import os 
import datetime
"""
The retry model gets a k based on the avearge file size divide by 4. (If the avagere file will be bigger then 4)
"""
class AverageMemory_k_segements(KSegmentsModel):
    
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
        
        for memoryFile,_,x in self.files:
            memoryArray = np.array(list(map(lambda d: (len(d['_value'])), memoryFile)))
            memoryValueTrainigsFile.append(memoryArray)
            
        sumUpK = 0
        
        for memoryArray in memoryValueTrainigsFile:
            
            sumUpK =+ self.findChangePoints(memoryArray)
        
        self.k = int(sumUpK / len(memoryArray))
        
        self.valid_k()
        pass
            
        
    def findChangePoints(self, memoryArray):
        avaerage = np.average(memoryArray)
        k = 0
        currentLow = True
        currentHigh = True
        for memoryLogSample in memoryArray:
            if memoryLogSample <= avaerage and currentHigh:
                k =+ 1
                currentLow = True
                currentHigh = False
            if memoryLogSample > avaerage and currentLow:
                k =+ 1
                currentHigh = True
                currentLow = False
        return k
                
    # divide to the 
    
    
    def valid_k(self):
        for y,_,x in self.files:
            if len(y) < self.k:
                self.k = len(y)