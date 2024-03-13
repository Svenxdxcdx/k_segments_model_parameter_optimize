from tsb_resource_allocation.k_segments_model import KSegmentsModel

import matplotlib.pyplot as plt
import numpy as np
import os 
import datetime


class MostFrequentK_MCP_k_segmetns(KSegmentsModel):
    
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
        self.mode = "MemoryLookUpTable" # fileEvents, interploate#


    def calculate_k(self):
        
        
        memoryValueTrainigsFile = list(map(lambda d: (d[0]['_value']), self.files))            
        
        k_list = []
        numberOf_k_list = []
        
        
        
        for memoryArray in memoryValueTrainigsFile:
            
            trainingsFile_k = self.findChangePoints(memoryArray)
            if trainingsFile_k in k_list:
                index = k_list.index(trainingsFile_k)
                numberOf_k_list[index] += 1
                
            else:
                
                
                k_list.append(trainingsFile_k)
                numberOf_k_list.append(1)
                
        indexMostOccur_k = numberOf_k_list.index(max(numberOf_k_list))
        self.k = k_list[indexMostOccur_k]
        self.valid_k()
        pass
    
    
    
    def valid_k(self):
        for y,_,x in self.files:
            if len(y) < self.k:
                self.k = len(y)
            
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
                