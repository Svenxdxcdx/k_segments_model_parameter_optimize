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

from tsb_resource_allocation.kSegementVariations.fileEvents_k_segements import FileEvents_k_segements

sns.set_theme(style="darkgrid")

class FileEvents_test(unittest.TestCase):
    
    def test_callsClass(self):
        pass
    

if __name__ == '__main__':
    unittest.main()