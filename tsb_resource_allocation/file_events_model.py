from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np
import datetime
import os

# File Events Model
# Author: Nils Diedrich (nils.diedrich@aol.de)

class FileEventsModel:

    def __init__(
            self,
            monotonically_increasing = True,
            default_value = 100
        ):
        self.monotonically_increasing = monotonically_increasing
        self.default_value = default_value
        self.files = []

    def predict(self, new_x):
        r = []
        for s in range(len(self.model_value)):
            p_v = self.model_value[s].predict(np.array([new_x]).reshape((-1,1))).astype(int)[0]
            p_t = self.model_time[s].predict(np.array([new_x]).reshape((-1,1))).astype(int)[0]
            if self.monotonically_increasing and len(r) > 0 and p_v < r[-1]:
                p_v = r[-1]
            if p_v <= 0:
                p_v = self.default_value
            if p_t <= 0:
                p_t = 1
            for i in range(p_t):
                r.append(p_v)
        return r
    
    def train_model(self):
        if len(self.files) == 0: 
            print("Training files are empty!")
            return -1
        
        # f:files = (0:value, 1:file_events, 2:total_input_file_size)
        
        data = list(map(lambda d: (d[0], self.filter_file_events(d[1]), d[2]), self.files))
        valid_dataset = all(len(d[1]) == len(data[0][1]) for d in data[1:])
        
        if not valid_dataset:
            #print("Invalid dataset!")
            return -1
        
        data = list(map(lambda d: (d[0],list(map(lambda f: self.find_file_event_in_values(d[0], f), d[1])),d[2]), data))
        
        self.x = []
        self.y_t = [[] for _ in range(len(data[0][1])+1)] 
        self.y_v = [[] for _ in range(len(data[0][1])+1)] 
        
        for y,z,x in data:
            self.x.append(x)
            z.append(len(y))
            y = y['_value']
            pointer = 0
            
            for i,cp in enumerate(z):
                s = y[pointer:cp]
                if len(s) == 0:
                    if cp > 0:
                        s = [y[cp]]
                    else:
                        s = [y[0]]
                pointer = cp
                self.y_t[i].append(len(s))
                self.y_v[i].append(max(s))
                
        self.model_time = list(map(lambda y: self.train_linear_model(self.x, y, 1), self.y_t))
        self.model_value = list(map(lambda y: self.train_linear_model(self.x, y, 0), self.y_v))
        
        
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

    def train_linear_model(self, x, y, mode):
        lm = LinearRegression()
        lm.fit(np.asarray(x).reshape((-1, 1)),y)
        l_diff = 0
        for i,v in enumerate(x):
            pred = lm.predict(np.array([v]).reshape((-1,1)))
            diff = y[i] - pred
            if mode == 0:
                l_diff = max(diff, l_diff)
            else:
                l_diff = min(diff, l_diff)
        lm.intercept_ += l_diff
        return lm

    def plot_time_regression(self, num_cluster):
        self.plot_regression(num_cluster, self.y_time, self.time_model)

    def plot_ram_regression(self, num_cluster):
        self.plot_regression(num_cluster, self.y_ram, self.ram_model)

    def plot_regression(self, num_cluster, y, model):
        plt.scatter(self.x, y[num_cluster], color='g')
        plt.plot(self.x, model[num_cluster].predict(np.asarray([self.x]).reshape((-1, 1))), color='r')
        

    
