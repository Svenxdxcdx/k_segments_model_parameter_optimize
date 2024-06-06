from tsb_resource_allocation.k_segments_model import KSegmentsModel

import matplotlib.pyplot as plt
import numpy as np
import os 
import datetime
from scipy.signal import find_peaks, peak_prominences, peak_widths, chirp

class PeakMemory_k_segments(KSegmentsModel):
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
        self.mode = "peakMemory" # fileEvents, interploate
        self.dir = ""
    # memory is the first
    def calculate_k(self):
        memoryList = list(map(lambda d: (d[0]['_value']), self.files))
        self.k = self.findAveragePeaks(memoryList)
        self.valid_k()
        pass
    
    def valid_k(self):
        for y,_,x in self.files:
            if len(y) < self.k:
                self.k = len(y)
        
    def findAveragePeaks(self, memoryList):
        numberOfFiles = len(memoryList)
        numberOfPeaksOverAllFiles = 0
        
        id = 0
        for memory in memoryList:
            peaks, _ = find_peaks(memory)
            prominences = peak_prominences(memory, peaks)[0]
            contour_heights = memory[peaks] - prominences
            results_full = peak_widths(memory, peaks, rel_height=0.5)
            id += 1
            numberOfPeaksOverAllFiles = numberOfPeaksOverAllFiles + len(peaks)
            
        memToPlot = memoryList[0]
        peaks, _ = find_peaks(memToPlot)
        prominences = peak_prominences(memToPlot, peaks)[0]
        contour_heights = memToPlot[peaks] - prominences
        results_full = peak_widths(memToPlot, peaks, rel_height=0.5)
        
        plt.figure()
        plt.plot(np.array(memToPlot))
        plt.plot(peaks, memToPlot[peaks], "x")
        #plt.hlines(*results_full[1:], color="green")
        
        #
        plt.vlines(x=peaks, ymin=contour_heights, ymax=memToPlot[peaks], color="red")
        
        plt.xlabel('Time in Seconds') 
        plt.ylabel("Time Series points")
        
        #plt.show()
        filePath = "plotsPng\\peaksExamples\\"+ self.dir[0]
        
        if os.path.exists(filePath + ".png"):
            os.remove(filePath + ".png")
        plt.savefig(filePath + '.png', dpi=100)
        plt.close()
        return int(numberOfPeaksOverAllFiles / numberOfFiles)
        
        
    def getFirstTrace(self, trace):
        trace
        pass