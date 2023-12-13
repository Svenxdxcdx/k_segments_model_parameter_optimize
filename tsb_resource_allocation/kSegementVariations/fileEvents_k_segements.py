from tsb_resource_allocation.k_segments_model import KSegmentsModel
from typing import override

class FileEvents_k_segements(KSegmentsModel):
    
    def __init__(
            self,
            monotonically_increasing = True,
            default_value = 100,
            k = 2,
            time_mode = 1,
        ):
        super.__init__(
            monotonically_increasing,
            default_value,
            k,
            time_mode)
        self.mode = "fileEvents" # fileEvents, interploate
        
    @override(KSegmentsModel)
    
    
    def calculate_k(self):
        return 
