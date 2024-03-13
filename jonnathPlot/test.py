BASE_DIR = 'C:\\privat\\Bachelor_Work\\pytonProject\\update-traces\\k-Segments-traces-main' 

import matplotlib.pyplot as plt
import seaborn as sns
import os
import math
import pandas as pd
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import random
import pickle
import sys
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
from tsb_resource_allocation.kSegementVariations.fileEvents_k_segments import FileEvents_k_segments
from tsb_resource_allocation.kSegementVariations.peakMemory_k_segments import PeakMemory_k_segments
sns.set_theme(style="darkgrid")

# Helper methods


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
    
    
    # FileEvents_k_segments
    task_model = FileEvents_k_segments(k = k, monotonically_increasing = monotonically_increasing)
    simulation = Simulation(task_model, directory, retry_mode = 'selective', provided_file_names = training)
    simulations.append(simulation)
    
    # KSegments retry: selective
    task_model = KSegmentsModel(k = k, monotonically_increasing = monotonically_increasing)
    simulation = Simulation(task_model, directory, retry_mode = 'selective', provided_file_names = training)
    simulations.append(simulation)
    
    # KSegments retry: selective - NO UNDERPREDICTION
    task_model = KSegmentsModel(k = k, monotonically_increasing = monotonically_increasing, time_mode = -1)
    simulation = Simulation(task_model, directory, retry_mode = 'selective', provided_file_names = training)
    #simulations.append(simulation)
    
    # KSegments retry: partial
    task_model = KSegmentsModel(k = k, monotonically_increasing = monotonically_increasing)
    simulation = Simulation(task_model, directory, retry_mode = 'partial', provided_file_names = training)
    simulations.append(simulation)
    
    
    selected_k ,waste, retries, runtimes = [0 for _ in range(len(simulations))],[0 for _ in range(len(simulations))],[0 for _ in range(len(simulations))],[0 for _ in range(len(simulations))]
    for file_name in test:
        for i,s in enumerate(simulations):
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


# OUTPUT = ( [Waste: [Witt: 25, Tovar: 25, k-segments:25], [50] , [75]], [Retries], [Runtime])
def benchmark_task(task_dir = '/eager/markduplicates', base_directory = BASE_DIR):
    directory = f'{base_directory}/{task_dir}'
    file_names_orig = []
    file_order = get_file_order(directory)
    if file_order != None:
        file_names_orig = file_order
    else:
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

def record_file_order(workflow_tasks, base_directory, depth):
    if depth > 1:
        return
    f = open(f"{base_directory}/file_order.txt", "w")
    for task in workflow_tasks:
        basename = os.path.basename(task)
        f.write(f"{basename}\n")
        if depth > 0:
            continue
        record_file_order(get_file_names(task), f'{base_directory}/{basename}', depth+1)
        
def get_file_order(base_directory):
    try:
        with open(f'{base_directory}/file_order.txt') as f:
            return f.read().splitlines()
    except:
        return None
    

if __name__ == "__main__":
    base_directory = f'{BASE_DIR}/sarek'
    base_directory_eager = f'{BASE_DIR}/eager'
    workflow_tasks = []
    file_order = get_file_order(base_directory)
    file_order_eager = get_file_order(base_directory_eager)
    if file_order != None:
        workflow_tasks_sarek = file_order
        workflow_tasks_eager = file_order_eager
        workflow_tasks = workflow_tasks_sarek + workflow_tasks_eager
        
    else:
        workflow_tasks = [os.path.join(base_directory, item) for item in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, item))]
        workflow_tasks = [task for task in workflow_tasks if len(os.listdir(task)) > 40]
        workflow_tasks = list(map(os.path.basename, workflow_tasks))



    categories = ["Wastage", "Retries", "Runtime"]
    percentages = ["25%", "50%", "75%"]

    total_waste = np.array([])
    total_retries = np.array([])
    total_runtime = np.array([])

    # 0 = WASTE, 1 = RETRIES, 2 = RUNTIME
    for task in workflow_tasks:
        
        if task in file_order:
            r = benchmark_task(task, base_directory)
        else:
            r = benchmark_task(task, base_directory_eager)
        
        if r == -1:
            continue
        
        r = [np.array(element) for element in r]
        task_name = os.path.basename(task)
        
        if 'total_waste' not in locals() or not len(total_waste) > 0 :
            total_waste = r[0]
            total_retries = r[1]
            total_runtime = r[2]
        else:
            total_waste += r[0]
            total_retries += r[1]
            total_runtime += r[2]
            
        
        m = ', '.join(map(str, r[0][2]))
        print(f'{task_name}')
        for i, category in enumerate(categories): 
            for j, percentage in enumerate(percentages): 
                print(f'{category} {percentage}: {r[i][j]}')
                
    total_waste = total_waste / 33
    total_retries = total_retries / 33
    total_runtime = total_runtime / 33
    print(total_waste)
    print(total_retries)
    print(total_runtime)
    

    categories = ['PeakMemory_k_segments', 'FileEvents_k_segments','k-Segments Selective', 'k-Segments Partial']
    hue_labels = ['25%', '50%', '75%']
    flattened_data = []

    for hue_index, array in enumerate(total_waste):
        for category_index, value in enumerate(array):
            flattened_data.append({'Category': categories[category_index], 'Value': value, 'Hue': hue_labels[hue_index]})

    df = pd.DataFrame(flattened_data)

    # Plot using seaborn
    sns.barplot(data=df, x='Category', y='Value', hue='Hue')
    plt.title('Bar Plot with Hues')
    plt.ylabel('Values')
    plt.xlabel('Categories')
    plt.legend(title='Hue')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Show the plot
    plt.show()