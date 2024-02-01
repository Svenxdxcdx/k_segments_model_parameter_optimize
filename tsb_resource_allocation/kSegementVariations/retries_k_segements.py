from tsb_resource_allocation.k_segments_model import KSegmentsModel

import matplotlib.pyplot as plt
import numpy as np
import os 
import datetime
"""_summary_
The retry model increases the k with every simulation to try reach better stats for storeage waste. 
This is happing with a limit for 25% 4 retries, for 50% 6 retries and for 75% 8 retries.

"""
class Retries_k_segements(KSegmentsModel):
    
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
        self.mode = "retries" # fileEvents, interploate
        self.retryCounter = 0