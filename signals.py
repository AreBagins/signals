# signals.py (poprawiony)
import numpy as np
import matplotlib.pyplot as plt
import re

# Słownik z opisami sygnałów (używany także w main.py)
SIGNAL_DESCRIPTIONS = {
    "S1": "Szum o rozkładzie jednostajnym",
    "S2": "Szum gaussowski",
    "S3": "Sygnał sinusoidalny",
    "S4": "Sygnał sinusoidalny wyprostowany jednopołówkowo",
    "S5": "Sygnał sinusoidalny wyprostowany dwupołówkowo",
    "S6": "Sygnał prostokątny",
    "S7": "Sygnał prostokątny symetryczny",
    "S8": "Sygnał trójkątny",
    "S9": "Skok jednostkowy",
    "S10": "Impuls jednostkowy (delta Kroneckera)",
    "S11": "Szum impulsowy"
}


class Signal:
    def __init__(self, type_name):
        self.signal_type = type_name
        self.samples = None
        self.t = None

    def draw_plot(self):
        if self.samples is None:
            return
        plt.figure(figsize=(10, 4))
        plt.axhline(color='b', ls='--')
        plt.axvline(color='b', ls='--')
        plt.plot(self.t, self.samples, 'ro', markersize=1)
        plt.title(f"Sygnał: {translate(self.signal_type)}")
        plt.xlabel("t [s]")
        plt.ylabel("Amplituda")
        plt.grid(True)
        plt.show()

    def draw_hist(self, bins):
        if self.samples is None:
            return
        x = self.samples
        # Dla sygnałów okresowych – przycinamy do pełnych okresów
        if hasattr(self, 'T') and self.T is not None and self.T > 0:
            samples_per_period = int(round(self.T * self.fs))
            if samples_per_period > 0:
                n_full_periods = len(x) // samples_per_period
                if n_full_periods > 0:
                    print("Uwzględniono tylko pełne okresy.")
                    x = x[:n_full_periods * samples_per_period]
        plt.figure(figsize=(10, 4))
        plt.hist(x, bins, rwidth=0.9)
        plt.title(f"Sygnał: {translate(self.signal_type)}")
        plt.xlabel("Wartość")
        plt.ylabel("Ilość próbek")
        plt.show()


class ContinousSignal(Signal):
    def __init__(self, type_name, A, t1, d, T=None, kw=None, ts=None):
        super().__init__(type_name)
        self.A = A
        self.t1 = t1
        self.d = d
        self.T = T
        self.kw = kw
        self.ts = ts

    def to_discrete(self, fs):
        n_samples = int(np.ceil(self.d * fs))
        t = self.t1 + np.arange(n_samples) / fs
        if len(t) > n_samples:
            t = t[:n_samples]

        A = self.A
        T = self.T
        kw = self.kw
        ts = self.ts
        t1 = self.t1

        if self.signal_type == "S1":
            samples = np.random.uniform(-A, A, len(t))
        elif self.signal_type == "S2":
            samples = np.random.normal(0, A / 3, len(t))
        elif self.signal_type == "S3":
            samples = A * np.sin(2 * np.pi * (1 / T) * (t - t1))
        elif self.signal_type == "S4":
            sin_val = np.sin((2 * np.pi / T) * (t - t1))
            samples = 0.5 * A * (sin_val + np.abs(sin_val))
        elif self.signal_type == "S5":
            samples = A * np.abs(np.sin((2 * np.pi / T) * (t - t1)))
        elif self.signal_type == "S6":
            samples = np.where(((t - t1) % T) < (kw * T), A, 0.0)
        elif self.signal_type == "S7":
            samples = np.where(((t - t1) % T) < (kw * T), A, -A)
        elif self.signal_type == "S8":
            term = (t - t1) % T
            samples = np.where(term < kw * T,
                               (A / (kw * T)) * term,
                               (-A / (T * (1 - kw))) * (term - T))
        elif self.signal_type == "S9":
            samples = np.zeros_like(t)
            samples[t > ts] = A
            samples[np.isclose(t, ts)] = A / 2
        else:
            samples = np.zeros_like(t)

        T_param = T if self.signal_type in ["S3", "S4", "S5", "S6", "S7", "S8"] else None
        return DiscreteSignal(f"{self.signal_type}", self.A,
                              self.t1, self.d, fs, samples=samples, T=T_param)


class DiscreteSignal(Signal):
    def __init__(self, type_name, A, t1, d, fs, p=None, samples=None, T=None):
        super().__init__(type_name)
        self.t1 = t1
        self.fs = fs
        self.T = T
        if samples is not None:
            self.samples = np.array(samples)
        elif type_name == "S10":
            n = int(d * fs)
            if n <= 0:
                raise ValueError("Liczba próbek musi być dodatnia.")
            self.samples = np.zeros(n)
            if p < n:
                self.samples[p] = A
        elif type_name == "S11":
            n = int(d * fs)
            self.samples = np.where(np.random.rand(n) < p, A, 0.0)
        else:
            self.samples = np.array([])
        self.t = t1 + np.arange(len(self.samples)) / fs

    def calculate_parameters(self):
        x = self.samples
        if self.T is not None and self.T > 0:
            samples_per_period = int(round(self.T * self.fs))
            if samples_per_period > 0:
                n_full_periods = len(x) // samples_per_period
                if n_full_periods > 0:
                    x = x[:n_full_periods * samples_per_period]
        mean = np.mean(x)
        abs_mean = np.mean(np.abs(x))
        var = np.var(x)
        power = np.mean(x ** 2)
        return {"Średnia": mean, "Śr. Bezwzględna": abs_mean,
                "Wariancja": var, "Moc": power, "RMS": np.sqrt(power)}

    def _align(self, other):
        if not isinstance(other, DiscreteSignal):
            raise TypeError("Operacja możliwa tylko z innym DiscreteSignal")
        if self.fs != other.fs:
            raise ValueError("Sygnały muszą mieć tę samą częstotliwość próbkowania")
        if self.t1 != other.t1:
            raise ValueError("Sygnały muszą mieć ten sam czas początkowy t1")
        min_len = min(len(self.samples), len(other.samples))
        return self.samples[:min_len], other.samples[:min_len], self.t1, self.fs

    def __add__(self, other):
        s1, s2, t1, fs = self._align(other)
        result_samples = s1 + s2
        d = len(result_samples) / fs
        return DiscreteSignal(f"{self.signal_type}+{other.signal_type}", 0, t1, d, fs, samples=result_samples)

    def __sub__(self, other):
        s1, s2, t1, fs = self._align(other)
        result_samples = s1 - s2
        d = len(result_samples) / fs
        return DiscreteSignal(f"{self.signal_type}-{other.signal_type}", 0, t1, d, fs, samples=result_samples)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            result_samples = self.samples * other
            d = len(result_samples) / self.fs
            return DiscreteSignal(f"{self.signal_type}*{other}", 0, self.t1, d, self.fs, samples=result_samples)
        elif isinstance(other, DiscreteSignal):
            s1, s2, t1, fs = self._align(other)
            result_samples = s1 * s2
            d = len(result_samples) / fs
            return DiscreteSignal(f"{self.signal_type}*{other.signal_type}", 0, t1, d, fs, samples=result_samples)
        else:
            raise TypeError("Nieobsługiwany typ dla mnożenia")

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("Dzielenie przez zero")
            result_samples = self.samples / other
            d = len(result_samples) / self.fs
            return DiscreteSignal(f"{self.signal_type}/{other}", 0, self.t1, d, self.fs, samples=result_samples)
        elif isinstance(other, DiscreteSignal):
            s1, s2, t1, fs = self._align(other)
            with np.errstate(divide='ignore', invalid='ignore'):
                result_samples = np.divide(s1, s2, where=s2 != 0, out=np.zeros_like(s1))
                result_samples[np.abs(s2) < 1e-12] = 0
            d = len(result_samples) / fs
            return DiscreteSignal(f"{self.signal_type}/{other.signal_type}", 0, t1, d, fs, samples=result_samples)
        else:
            raise TypeError("Nieobsługiwany typ dla dzielenia")

    def __rmul__(self, other):
        return self.__mul__(other)


def translate(text: str) -> str:
    """Zamienia kod sygnału na opis (działa również na złożonych napisach)."""
    sorted_keys = sorted(SIGNAL_DESCRIPTIONS.keys(), key=len, reverse=True)
    pattern = re.compile('|'.join(re.escape(k) for k in sorted_keys))
    return pattern.sub(lambda m: SIGNAL_DESCRIPTIONS[m.group(0)], text)