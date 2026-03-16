import numpy as np

class Signal:
    def __init__(self,type):
        self.signal_type = type
    def is_continous(self):
        return False
   
    def draw_plot(self):
        print("plot")

    def draw_histogram(self,range):
        print(range)

    def save(self,path):
        print("saved")

    def calculate_parameters(self):
        return 0

class ContinousSignal(Signal):
    def __init__(self,type,amplitude,start_time,duration,period,fullness,jump_time):
        super().__init__(type)
        self.A = amplitude
        self.t1 = start_time
        self.d = duration
        self.T = period
        self.k = fullness
        self.ts = jump_time
        #Reszta parametrów do wyliczenia
    def discreticise(self):
        return DiscreteSignal()
    def is_continous(self):
        return True
    def calculate_parameters(self):
        return 1
    def save(self,path):
        print("saved discreticised signal")

class DiscreteSignal(Signal):
    def __init__(self,type,amplitude,first_sample,start_time,jump_sample,sampling_freq,duration,propability):
        super().__init__(type)
        self.A = amplitude
        self.n1 = first_sample
        self.t1 = start_time
        self.ns = jump_sample
        self.f = sampling_freq
        self.d = duration
        self.p = propability
        self.samples = np.empty()

    def __init__(self,sample_array):
        self.samples = sample_array

    def __add__(self, other):
        pass
    def __sub__(self, other):
        pass
    def __mul__(self, other):
        pass
    def __truediv__(self, other):
        pass
