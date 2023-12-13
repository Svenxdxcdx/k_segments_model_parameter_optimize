from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np
import math

# Witt Task Model
# Author: Nils Diedrich (nils.diedrich@aol.de)

class WittTaskModel:

    def __init__(
            self,
            mode = "mean", # mean and max
            d = 100
        ):
        self.d = d
        self.mode = mode
        self.files = []

    def predict(self, new_x):
        ram = self.model.predict(np.array([new_x]).reshape((-1,1))).astype(int)[0]
        if ram <= 0:
            ram = self.d
        return ram
    
    def train_model(self):
        if len(self.files) == 0: 
            print("Training files are empty!")
            return
        self.x = []
        self.y = []
        
        for file in self.files:
            self.x.append(file[2])
            self.y.append(file[0]['_value'].max())
        
        lm = self.train_linear_model(self.x, self.y)
        
        if self.mode == "mean-":
            intercept_shift = self.lr_mean_negative_shift(self.x,self.y,lm)
        elif self.mode == "mean+-":
            intercept_shift = self.lr_mean_shift(self.x,self.y,lm)
        else:
            intercept_shift = self.lr_max_shift(self.x,self.y,lm)
        lm.intercept_ += intercept_shift
        self.model = lm
        
    def lr_max_shift(self, x, y, model):
        l_diff = 0
        for i,v in enumerate(x):
            pred = model.predict(np.array([v]).reshape((-1,1)))
            diff = y[i] - pred
            l_diff = min(diff, l_diff)
        return abs(l_diff)
    
    def lr_mean_shift(self, x, y, model):
        s = 0 
        for i,v in enumerate(x):
            f_x = model.predict(np.array([v]).reshape((-1,1)))
            s += (f_x - y[i]) ** 2
        res = math.sqrt(s/(len(y) - 1))
        return res

    def lr_mean_negative_shift(self, x, y, model):
        s = 0 
        c = 0
        for i,v in enumerate(x):
            f_x = model.predict(np.array([v]).reshape((-1,1)))
            if f_x < y[i]:
                c += 1
                s += (f_x - y[i]) ** 2
        if c < 2:
            c = 2
        res = math.sqrt(s/(c-1))
        return res
        
        

    def train_linear_model(self, x, y):
        lm = LinearRegression()
        lm.fit(np.asarray(x).reshape((-1, 1)),y)
        return lm
    

    def plot_regression(self):
        plt.scatter(self.x, self.y, color='g')
        plt.plot(self.x, self.model.predict(np.asarray([self.x]).reshape((-1, 1))), color='r')
        

    
