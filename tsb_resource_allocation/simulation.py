from .k_segments_model import KSegmentsModel
from .file_events_model import FileEventsModel
from .default_model import DefaultModel
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import copy
import os

# Simulation
# Author: Nils Diedrich (nils.diedrich@aol.de)

class Simulation:
    
    def __init__(
            self,
            task_model,
            directory,
            retry_factor = 2,
            retry_mode = "full",
            max_mem = 128, # in GB
            provided_file_names = []
        ):
        self.task_model = task_model
        self.directory = directory
        self.retry_factor = retry_factor
        self.retry_mode = retry_mode
        self.max_mem = max_mem
        self.files = [] # [[MEMORY, FILE_EVENTS, INPUT_TOTAL_SIZE]]
        self.provided_file_names = provided_file_names
        file_names = self.get_file_names() if not provided_file_names else provided_file_names
        for file_name in file_names:
            memory = self.read_influx_csv(file_name, "_memory.csv")
            file_events = self.read_influx_csv(file_name, "_file_event.csv")
            metadata = self.read_influx_csv(file_name, "_metadata.csv")
            input_total_size = metadata.query('_field == "files_input_total_size"')['_value'].iloc[0]
            self.files.append([memory, file_events, input_total_size])
        self.task_model.files = self.files
        # TODO
        if isinstance(self.task_model, KSegmentsModel) and self.task_model.mode != "normal":
            #if mod
            pass
        if self.task_model.mode == "peakMemory":
            self.task_model.dir = file_names
        self.error = self.task_model.train_model()
        
    def get_file_names(self):
        return [name.rsplit('_',1)[0] for name in os.listdir(self.directory) if not os.path.isdir(f"{self.directory}{name}") and name.endswith("_memory.csv")]
    
    def read_influx_csv(self, file_name, ending):
        csv_content = pd.read_csv(f'{self.directory}/{file_name+ending}', skiprows = 3)
        return csv_content

    def execute(self, test_file_name, suppress_plots = True):
        if self.error:
            return (-1,-1,-1)
        base_directory = self.directory+"/test" if not self.provided_file_names else self.directory
        memory = pd.read_csv(f'{base_directory}/{test_file_name}_memory.csv', skiprows=3)
        file_events = pd.read_csv(f'{base_directory}/{test_file_name}_file_event.csv', skiprows=3)
        data = memory["_value"]
        metadata = pd.read_csv(f'{base_directory}/{test_file_name}_metadata.csv', skiprows=3)
        input_total_size = metadata.query('_field == "files_input_total_size"')['_value'].iloc[0]
        default_value = (metadata.query('_field == "max_mem"')['_value'].iloc[0]) / (1024 * 1024)
        if isinstance(self.task_model, KSegmentsModel) or isinstance(self.task_model, FileEventsModel):
            pts = self.task_model.predict(input_total_size)
            clusters = self.get_clusters(pts)
            if self.task_model.mode == "activeFeedbackModel":
                self.task_model.evaluteData(data, [memory, file_events, input_total_size])
        else:
            if isinstance(self.task_model, DefaultModel):
                prediction = default_value
            else:
                prediction = self.task_model.predict(input_total_size)
            pts = []
            for i in range(len(data)):
                pts.append(prediction)
        if not suppress_plots:
            plt.plot(data)
        waste = 0
        runtime = 0
        retries = 0
        success = False
        while(not success):
            if not suppress_plots:
                plt.plot(pts)
            simulation = self.simulate(data, pts)
            success = simulation[0]
            
            waste += simulation[1]
            failed_at = simulation[2]
            runtime += simulation[2] + 1
            retries += 1
            
            if self.retry_mode == "full":
                pts = list(map(lambda x: x*self.retry_factor, pts))
            elif self.retry_mode == "tovar":
                pts = list(map(lambda x: self.max_mem * 1000, pts))
            elif self.retry_mode == "selective":
                pts = self.selective_retry(pts, failed_at, clusters)
            elif self.retry_mode == "partial":
                pts = self.partial_retry(pts, failed_at, clusters)
                
        return waste, retries-1, runtime
    
    def get_clusters(self, pts):
        cur = pts[0]
        last_i = 0
        clusters = []
        for i,v in enumerate(pts):
            if cur != v:
                clusters.append((last_i, i-1))
                cur = v
                last_i = i
        clusters.append((last_i, i))
        return clusters

    def selective_retry(self, pts, failed_at, clusters):
        if failed_at > clusters[-1][1]:
            for i in range(clusters[-1][0], clusters[-1][1]+1):
                pts[i] = pts[i] * self.retry_factor
            return pts
        for cluster in clusters:
            if cluster[0] <= failed_at and cluster[1] >= failed_at:
                for i in range(cluster[0], cluster[1]+1):
                    pts[i] = pts[i] * self.retry_factor
                break
        return pts
    
    def partial_retry(self, pts, failed_at, clusters):
        if failed_at > clusters[-1][1]:
            for i in range(clusters[-1][0], clusters[-1][1]+1):
                pts[i] = pts[i] * 2
            return pts
        for cluster in clusters:
            if cluster[1] >= failed_at:
                for i in range(cluster[0], cluster[1]+1):
                    pts[i] = pts[i] * self.retry_factor
        return pts
    
    # Author Sven Hoferichter
    # TODO new mathod
    def selectiveAreaRetry(self, pts, failed_at, clusters):
        pass
    
    def simulate(self, ts, pts): # return True or False and waste 
        c_pts = copy.deepcopy(pts)
        while len(c_pts) < len(ts):
            c_pts.append(pts[-1])
        
        for i,v in ts.items():
            if v > c_pts[i]:
                return (False, self.calc_resource_wastage_penalty(c_pts[:i+1]), i)
        return (True, self.calc_resource_wastage(ts,c_pts[:len(ts)]), len(ts))
    
    def calc_resource_wastage(self, its, pts):
        pts_i = np.trapz(pts)
        its_i = np.trapz(its)
        diff = pts_i - its_i
        return diff
    
    def calc_resource_wastage_penalty(self, pts):
        return np.trapz(pts)