from tsb_resource_allocation.k_segments_model import KSegmentsModel

import matplotlib.pyplot as plt
import numpy as np
import os 
import datetime


class ActiveFeedbackModel_k_segements(KSegmentsModel):
    
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
        self.mode = "activeFeedbackModel" 
        
        
    def calculate_k(self):
        memoryLenList = list(map(lambda d: (len(d[0]['_value'])), self.files))
        self.k = self.find_k_withMemoryLogFileSize(memoryLenList)
        
    
        