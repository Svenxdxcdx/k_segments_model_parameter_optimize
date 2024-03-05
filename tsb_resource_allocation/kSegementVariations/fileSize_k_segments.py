from tsb_resource_allocation.k_segments_model import KSegmentsModel

import matplotlib.pyplot as plt
import numpy as np
import os 
import datetime
"""
The retry model gets a k based on the avearge file size divide by 4. (If the avagere file will be bigger then 4)
"""
class FileSize_k_segments(KSegmentsModel):
    
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
        memoryLenList = list(map(lambda d: (len(d[0]['_value'])), self.files))
        self.k = self.find_k_withMemoryLogFileSize(memoryLenList)
        
    # divide to the 
    def find_k_withMemoryLogFileSize(self, memoryLenList):
        memoryLenList.sort()
        smallestSize = memoryLenList[0]
        memoryArray = np.array(memoryLenList)
        mean = int(np.mean(memoryArray))
        k = int(mean / 4)
        if k <= smallestSize:
            return k
        else:
            return smallestSize
        
    
    def valid_k(self):
        for y,_,x in self.files:
            if len(y) < self.k:
                self.k = len(y)

    
      