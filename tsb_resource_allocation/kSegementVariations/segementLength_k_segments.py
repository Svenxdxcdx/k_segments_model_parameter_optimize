from tsb_resource_allocation.k_segments_model import KSegmentsModel

import matplotlib.pyplot as plt
import numpy as np
import os 
import datetime


BASE_MODLE_TRAININGS_K = 4

class SegementLength_k_segements(KSegmentsModel):
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
        segmentLength = int(len(smallestMemoryLog) / BASE_MODLE_TRAININGS_K)
        numberOfAllSegments = 0
        for memoryLog in memoryList:
            numberOfSegments = int(len(memoryLog) / segmentLength)
            numberOfAllSegments += numberOfSegments
            
        self.k = int(numberOfAllSegments / len(memoryList))
        self.valid_k()
        pass
    
    
    
    def valid_k(self):
        for y,_,x in self.files:
            if len(y) < self.k:
                self.k = len(y)
        
