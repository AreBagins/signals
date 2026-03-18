import numpy as np
import matplotlib.pyplot as plt

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

    def draw_plot(self):
        print("plot")

    def draw_histogram(self,range):
        print(range)

class DiscreteSignal(Signal):
    def __init__(self, *args, **kwargs):
            if(len(args)==8):
                super().__init__(args[0])
                self.A = args[1]
                self.n1 = args[2]
                self.t1 = args[3]
                self.ns = args[4]
                self.f = args[5]
                self.d = args[6]
                self.p = args[7]
                if(self.signal_type=="K"):
                    #Postać tablicy sygnałów:
                    #Rząd 0: czas pobrania próbki(n)
                    #Rząd 1: wartość sygnału w n
                    self.samples = np.zeros((2,int(25*self.f)))
                    for col in range(self.samples.shape[1]):
                        self.samples[0,col]=self.n1+col*(1/self.f)
                        if(self.samples[0,col]==self.ns):
                            self.samples[1,col]=self.A
                        else:
                            self.samples[1,col]=0
                else:
                    self.samples = np.empty()
            elif(len(args)==1):
                    self.samples = args[1]
            else:
                print("Wrong amount of params")
    def __add__(self, other):
        pass
    def __sub__(self, other):
        pass
    def __mul__(self, other):
        pass
    def __truediv__(self, other):
        pass

    def draw_plot(self):
        fig, ax = plt.subplots()
        ax.axhline(color='b',ls='--')
        ax.axvline(color='b',ls='--')
        ax.plot(self.samples[0,:], self.samples[1,:],'ro')
        ax.set(xlabel='t (s)', ylabel='A')
        plt.show()

    def draw_histogram(self,range):
        print(range)
