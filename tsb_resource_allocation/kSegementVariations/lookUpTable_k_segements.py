from tsb_resource_allocation.k_segments_model import KSegmentsModel

import matplotlib.pyplot as plt
import numpy as np
import os 
import datetime
"""_summary_
The retry model increases the k with a look up table. The look up table is based with different k, for example low, mid and high.
The selection is based on the procent parts of file size. For example if mainly small size files exists, the modle take from the look 
up table a k form from the low part. 

range 
"""

NUMBER_OF_PARTS = 10
START_K = 4

class LookUpTable_k_segements(KSegmentsModel):
    
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
        self.mode = "lookUpTable" # fileEvents, interploate#
        
    def calculate_k(self):
        memoryLenList = list(map(lambda d: (len(d[0]['_value'])), self.files))
        self.k = self.buildLookUpTable(memoryLenList)
        if self.k == 0:
            self.k = 1
        
    # Numeric misstake get covered
    def buildLookUpTable(self, memoryLenList):
        memoryLenList.sort()
        smallestSize = memoryLenList[0]
        
        max_k = smallestSize
        
        biggestSize = memoryLenList[len(memoryLenList)-1]
        sizeDifference = biggestSize - smallestSize
        partsSize = sizeDifference / NUMBER_OF_PARTS
        
        partsCounterArray = np.zeros(10)
        for mermoryLen in memoryLenList:
            for factor in range (0, NUMBER_OF_PARTS):
                if factor == NUMBER_OF_PARTS - 1:
                    partsCounterArray[factor] += 1
                    break
                currentPart = factor*partsSize + (smallestSize + partsSize)
                if mermoryLen < currentPart:
                    partsCounterArray[factor] += 1
                    break
        
        strongestFileSizeIndex = np.argmax(partsCounterArray)
        return self.selectLookUpTablePart(smallestSize, strongestFileSizeIndex)
    
    
    def selectLookUpTablePart(self, smallestSize, strongestFileSizeIndex):
        return int((smallestSize / NUMBER_OF_PARTS) * (strongestFileSizeIndex+1))
    
    def selectK(self):
        pass