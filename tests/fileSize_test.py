import unittest
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import os
import math
import pandas as pd

PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(
    PROJECT_PATH
)
sys.path.append(SOURCE_PATH)



from tsb_resource_allocation.witt_task_model import WittTaskModel
from tsb_resource_allocation.tovar_task_model import TovarTaskModel
from tsb_resource_allocation.simulation import Simulation
from tsb_resource_allocation.k_segments_model import KSegmentsModel
from tsb_resource_allocation.file_events_model import FileEventsModel
from tsb_resource_allocation.default_model import DefaultModel

from tsb_resource_allocation.kSegementVariations.fileSize_k_segements import FileSize_k_segements

sns.set_theme(style="darkgrid")

class FileSize_test(unittest.TestCase):
    
    def test_run(self):
        
        directory = "C:/privat/Bachelor_Work/pytonProject/k-segments-traces-main/k-segments-traces-main/sarek\\BWAMEM1_MEM"
        file_names_orig = get_file_names(directory)

        percentages = [0.25, 0.5, 0.75]

        x = []
        y_waste = []
        y_retries = []
        y_runtime = []

        file_names = list(filter(lambda x: len(pd.read_csv(f'{directory}/{x}_memory.csv', skiprows = 3)) >= 8, file_names_orig))
        if len(file_names) == 0:
            return -1
        print(f'Usable Data: {len(file_names)}/{len(file_names_orig)}')
        
        for i in [ int(len(file_names)*p) for p in percentages ]:
            training = file_names[:i]
            test = file_names[i:] # file_names[i:] - other mode
            print(f"training: {len(training)}, test: {len(test)}",end="\r", flush=True)
            avg_waste, avg_retries, avg_runtime = run_simulation02(directory, training, test, k = 4)
            x.append(i)
            y_waste.append(list(map(lambda w: round(w, 2),avg_waste)))
            y_retries.append(avg_retries)
            y_runtime.append(avg_runtime)

        return (y_waste, y_retries, y_runtime)
            
    
    
        
def get_file_names(directory, number_of_files = -1):
    file_names = [name.rsplit('_',1)[0] for name in os.listdir(directory) if not os.path.isdir(f"{directory}{name}") and name.endswith("_memory.csv")]
    if number_of_files != -1:
        return file_names[:number_of_files]
    return file_names    

def run_simulation02(directory, training, test, monotonically_increasing = True, k = 4, collection_interval = 2):
    
    # MODELS
    simulations = []
    
    # KSegments retry: selective

    task_model = FileSize_k_segements(k = k, monotonically_increasing = monotonically_increasing)
    simulation = Simulation(task_model, directory, retry_mode = 'selective', provided_file_names = training)
    simulations.append(simulation)

    

    waste, retries, runtimes = [0 for _ in range(len(simulations))],[0 for _ in range(len(simulations))],[0 for _ in range(len(simulations))]
    for file_name in test:
        for i,s in enumerate(simulations):
            result = s.execute(file_name, True)
            waste[i] += ((result[0]/1000) * collection_interval)
            retries[i] += result[1]
            runtimes[i] += (result[2] * collection_interval)
    
    avg_waste = list(map(lambda w: w / len(test), waste))
    avg_retries = list(map(lambda r: r / len(test), retries))
    avg_runtime = list(map(lambda r: r / len(test), runtimes))
    
    return avg_waste, avg_retries, avg_runtime



if __name__ == '__main__':
    unittest.main()