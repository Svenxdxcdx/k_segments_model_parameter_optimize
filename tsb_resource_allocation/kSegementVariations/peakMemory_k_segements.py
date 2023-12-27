from tsb_resource_allocation.k_segments_model import KSegmentsModel

import matplotlib.pyplot as plt
import numpy as np
import os 
import datetime
from scipy.signal import find_peaks

class PeakMemory_k_segemnts(KSegmentsModel):
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
        self.k = self.findAveragePeaks(memoryList)
        
        pass
    
    def findAveragePeaks(self, memoryList):
        numberOfFiles = len(memoryList)
        numberOfPeaksOverAllFiles = 0
        
        for memory in memoryList:
            peaks, _ = find_peaks(memory)
            numberOfPeaksOverAllFiles = numberOfPeaksOverAllFiles + len(peaks)
        
        return int(numberOfPeaksOverAllFiles / numberOfFiles)
        
        
    def getFirstTrace(self, trace):
        trace
        pass