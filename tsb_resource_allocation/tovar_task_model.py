from .FirstAllocation import FirstAllocation

# Witt Task Model
# Author: Nils Diedrich (nils.diedrich@aol.de)
# First Allocation Source Code from: https://github.com/btovar/efficient-resource-allocations

class TovarTaskModel:

    def __init__(self):
        self.fa = FirstAllocation(name = "my memory usage")
        self.files = []
        pass

    def train_model(self):
        for file in self.files:
            data = file[0]["_value"]
            self.fa.add_data_point(value=data.max(), time=len(data))

    def predict(self, x):
        return self.fa.first_allocation(mode = 'waste')