

BASE_DIR = 'C:/privat/Bachelor_Work/pytonProject/k-segments-traces-main/k-segments-traces-main' 

import matplotlib.pyplot as plt
import seaborn as sns
import os
import math
import pandas as pd
from tsb_resource_allocation.witt_task_model import WittTaskModel
from tsb_resource_allocation.tovar_task_model import TovarTaskModel
from tsb_resource_allocation.simulation import Simulation
from tsb_resource_allocation.k_segments_model import KSegmentsModel
from tsb_resource_allocation.file_events_model import FileEventsModel
from tsb_resource_allocation.default_model import DefaultModel
from tsb_resource_allocation.kSegementVariations.fileEvents_k_segments import FileEvents_k_segments
from tsb_resource_allocation.kSegementVariations.peakMemory_k_segments import PeakMemory_k_segments
sns.set_theme(style="darkgrid")


PROJECT_PATH = os.getcwd()

def get_file_names(directory, number_of_files = -1):
    file_names = [name.rsplit('_',1)[0] for name in os.listdir(directory) if not os.path.isdir(f"{directory}{name}") and name.endswith("_memory.csv")]
    if number_of_files != -1:
        return file_names[:number_of_files]
    return file_names

def run_simulation(directory, training, test, monotonically_increasing = True, k = 4, collection_interval = 2):
    
    # MODELS
    simulations = []
    
    # PeakMemory_k_segments 
    task_model = PeakMemory_k_segments(k = k, monotonically_increasing = monotonically_increasing)
    simulation = Simulation(task_model, directory, retry_mode = 'selective', provided_file_names = training)
    simulations.append(simulation)
    
    
    selected_k ,waste, retries, runtimes = [0 for _ in range(len(simulations))],[0 for _ in range(len(simulations))],[0 for _ in range(len(simulations))],[0 for _ in range(len(simulations))]
    for file_name in test:
        for i,s in enumerate(simulations):
            # cute for reruns
            result = s.execute(file_name, True)
            if hasattr(s.task_model, 'k'):
                selected_k[i] = s.task_model.k
            waste[i] += ((result[0]/1000) * collection_interval)
            retries[i] += result[1]
            runtimes[i] += (result[2] * collection_interval)
    
    
    avg_waste = list(map(lambda w: w / len(test), waste))
    avg_retries = list(map(lambda r: r / len(test), retries))
    avg_runtime = list(map(lambda r: r / len(test), runtimes))
    
    return selected_k, avg_waste, avg_retries, avg_runtime


def benchmark_task(task_dir = f'{BASE_DIR}/eager/markduplicates'):
    directory = task_dir
    file_names_orig = get_file_names(directory)

    percentages = [0.25, 0.5, 0.75]

    x = []
    selected_k_List = []
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
        selected_k, avg_waste, avg_retries, avg_runtime = run_simulation(directory, training, test, k = 4)
        x.append(i)
        selected_k_List.append(selected_k)
        y_waste.append(list(map(lambda w: round(w, 2),avg_waste)))
        y_retries.append(avg_retries)
        y_runtime.append(avg_runtime)

    return (selected_k_List, y_waste, y_retries, y_runtime)




if __name__ == "__main__":
    base_directory = f'{BASE_DIR}/sarek'
    workflow_tasks = [os.path.join(base_directory, item) for item in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, item))]
    workflow_tasks = [task for task in workflow_tasks if len(os.listdir(task)) > 40]

    categories = ["selecktive k","Wastage", "Retries", "Runtime"]
    percentages = ["25%", "50%", "75%"]

    
    # 0 = WASTE, 1 = RETRIES, 2 = RUNTIME
    for task in workflow_tasks:
        r = benchmark_task(task)
        if r == -1:
            continue
        task_name = os.path.basename(task)
        m = ', '.join(map(str, r[0][2]))
        print(f'{task_name}')
        for i, category in enumerate(categories): 
            for j, percentage in enumerate(percentages): 
                print(f'{category} {percentage}: {r[i][j]}')