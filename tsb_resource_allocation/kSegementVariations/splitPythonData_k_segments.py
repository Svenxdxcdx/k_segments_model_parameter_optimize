import numpy as np
from sklearn.model_selection import train_test_split


from tsb_resource_allocation.k_segments_model import KSegmentsModel

import matplotlib.pyplot as plt
import numpy as np
import os 
import datetime
from scipy.signal import find_peaks, peak_prominences, peak_widths, chirp

class SplitPythonData_k_segments(KSegmentsModel):
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
        self.dir = ""
    # memory is the first
    def calculate_k(self):
        memoryList = list(map(lambda d: (d[0]['_value']), self.files))
        self.k = self.findAveragePeaks(memoryList)
        self.valid_k()
        pass
    
    def valid_k(self):
        for y,_,x in self.files:
            if len(y) < self.k:
                self.k = len(y)
        
    def findAveragePeaks(self, memoryList):
        numberOfFiles = len(memoryList)
        numberOfPeaksOverAllFiles = 0
        
        id = 0
        for memory in memoryList:
            pass
            
        return int(numberOfPeaksOverAllFiles / numberOfFiles)
        
        
    def getFirstTrace(self, trace):
        trace
        pass