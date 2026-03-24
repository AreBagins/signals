import numpy as np
import matplotlib.pyplot as plt


class Signal:
    def __init__(self, type_name):
        self.signal_type = type_name
        self.samples = None  # Amplitudy (y)
        self.t = None  # Czas (x)

    def draw_plot(self):
        if self.samples is None: return
        plt.figure(figsize=(10, 4))
        plt.plot(self.t, self.samples)
        plt.title(f"Sygnał: {self.signal_type}")
        plt.xlabel("t [s]")
        plt.ylabel("Amplituda")
        plt.grid(True)
        plt.show()


class ContinousSignal(Signal):
    def __init__(self, type_name, A, t1, d, T=None, kw=None, ts=None):
        super().__init__(type_name)
        self.A, self.t1, self.d, self.T, self.kw, self.ts = A, t1, d, T, kw, ts
        # "Udajemy" sygnał ciągły przez gęste próbkowanie (np. 1kHz)
        self.fs_internal = 1000
        self.t = np.arange(t1, t1 + d, 1 / self.fs_internal)
        self.samples = self._generate_values()

    def _generate_values(self):
        t, T, t1, kw, A, ts = self.t, self.T, self.t1, self.kw, self.A, self.ts
        if self.signal_type == "S4":  # Sin. jednopołówkowy
            sin_val = np.sin((2 * np.pi / T) * (t - t1))
            return 0.5 * A * (sin_val + np.abs(sin_val))
        elif self.signal_type == "S5":  # Sin. dwupołówkowy
            return A * np.abs(np.sin((2 * np.pi / T) * (t - t1)))
        elif self.signal_type == "S6":  # Prostokątny
            return np.where(((t - t1) % T) < (kw * T), A, 0.0)
        elif self.signal_type == "S7":  # Prostokątny symetryczny
            return np.where(((t - t1) % T) < (kw * T), A, -A)
        elif self.signal_type == "S8":  # Trójkątny
            term = (t - t1) % T
            return np.where(term < kw * T, (A / (kw * T)) * term, (-A / (T * (1 - kw))) * (term - T))
        elif self.signal_type == "S9":  # Skok jednostkowy
            res = np.zeros_like(t)
            res[t > ts] = A
            res[np.isclose(t, ts)] = A / 2
            return res
        return np.zeros_like(t)

    def calculate_parameters(self):
        x = self.samples
        periodic = ["S4", "S5", "S6", "S7", "S8"]
        if self.signal_type in periodic and self.T > 0:
            num_periods = int(self.d // self.T)
            if num_periods > 0:
                # Ucinamy do pełnych okresów wg instrukcji
                x = x[:int(num_periods * self.T * self.fs_internal)]

        mean = np.mean(x)
        abs_mean = np.mean(np.abs(x))
        var = np.var(x)
        pow_avg = np.mean(x ** 2)
        return {"Średnia": mean, "Śr. Bezwzględna": abs_mean, "Wariancja": var, "Moc": pow_avg, "RMS": np.sqrt(pow_avg)}


class DiscreteSignal(Signal):
    def __init__(self, type_name, A, t1, d, fs, p=None, samples=None):
        super().__init__(type_name)
        self.t1, self.fs = t1, fs
        if samples is not None:
            self.samples = np.array(samples)
        elif type_name == "S11":  # Szum impulsowy
            n = int(d * fs)
            self.samples = np.where(np.random.rand(n) < p, A, 0.0)
        self.t = t1 + np.arange(len(self.samples)) / fs

    def calculate_parameters(self):
        x = self.samples
        n = len(x)
        mean = np.sum(x) / n
        abs_mean = np.sum(np.abs(x)) / n
        var = np.sum((x - mean) ** 2) / n
        pow_avg = np.sum(x ** 2) / n
        return {"Średnia": mean, "Śr. Bezwzględna": abs_mean, "Wariancja": var, "Moc": pow_avg, "RMS": np.sqrt(pow_avg)}