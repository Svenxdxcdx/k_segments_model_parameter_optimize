from tsb_resource_allocation.k_segments_model import KSegmentsModel

import matplotlib.pyplot as plt
import numpy as np
import os 
import datetime
class FileEvents_k_segments(KSegmentsModel):
    
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
        self.mode = "fileEvents" # fileEvents, interploate
    
      
    
    def calculate_k(self):
        data = list(map(lambda d: (d[0], self.filter_file_events(d[1]), d[2]), self.files))
        
        valid_dataset = all(len(d[1]) == len(data[0][1]) for d in data[1:])
        if not valid_dataset:
            
            self.k = 4
            return 
        self.k = self.fileAvarageLength()
        return


    def fileAvarageLength(self):
        data = list(map(lambda d: (len(d[1])), self.files))
        numberOfFiles = len(data)
        numberOfAllFileEvents = 0
        
        for numberOfFileEvents in data:
            numberOfAllFileEvents = numberOfAllFileEvents + numberOfFileEvents 
        return int(numberOfAllFileEvents / numberOfFiles)
        
    
    
    def filter_file_events(self, file_events):
        paths = {}
        for i in range(0,len(file_events)):
            path = file_events['path'][i]
            _time = self.parse_timestamp(file_events['_time'][i])
            event_type = file_events['_value'][i]
            if event_type == 'DELETE':
                if path in paths.keys():
                    paths.pop(path,None)
            else:
                if not (os.path.split(path)[1].startswith('.')):
                    paths[path] = _time
        return sorted(paths.values())
        
    def find_file_event_in_values(self, values, file_event):
        for i in range(0, len(values)):
            if self.parse_timestamp(values["_time"][i]) > file_event:
                return i
        return len(values)-1
    
    def parse_timestamp(self, timestamp):
        diff = len(timestamp) - 26
        if diff > 0:
            timestamp = timestamp[:-diff]+'Z'
        if timestamp.endswith('.Z'):
            timestamp = timestamp[:-2]+'Z'
        return datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")