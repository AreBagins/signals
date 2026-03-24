import struct
import numpy as np
from signals import ContinousSignal, DiscreteSignal


class SignalApp:
    def __init__(self):
        self.active_signal = None

    def create_signal(self):
        print("\n--- GENERATOR (S4-S9, S11) ---")
        stype = input("Kod sygnału: ").upper()
        A = float(input("Amplituda (A): "))
        t1 = float(input("Czas pocz. (t1): "))
        d = float(input("Czas trwania (d): "))

        if stype == "S11":
            fs = float(input("Częstotliwość próbkowania (fs): "))
            p = float(input("Prawdopodobieństwo (p): "))
            self.active_signal = DiscreteSignal("S11", A, t1, d, fs, p=p)
        else:
            T = float(input("Okres (T): ")) if stype in ["S4", "S5", "S6", "S7", "S8"] else None
            kw = float(input("Wypełnienie (kw): ")) if stype in ["S6", "S7", "S8"] else None
            ts = float(input("Czas skoku (ts): ")) if stype == "S9" else None
            self.active_signal = ContinousSignal(stype, A, t1, d, T, kw, ts)
        print("Utworzono sygnał.")

    def save_binary(self):
        if not self.active_signal: return
        fname = input("Nazwa pliku (.bin): ")
        fs = float(input("Częstotliwość próbkowania do zapisu: "))

        # Dyskretyzacja "w locie" dla sygnałów ciągłych
        if isinstance(self.active_signal, ContinousSignal):
            t_disc = self.active_signal.t1 + np.arange(int(self.active_signal.d * fs)) / fs
            samples = np.interp(t_disc, self.active_signal.t, self.active_signal.samples)
            t1 = self.active_signal.t1
        else:
            samples = self.active_signal.samples
            t1 = self.active_signal.t1
            fs = self.active_signal.fs

        with open(fname, 'wb') as f:
            # Nagłówek: t1(d), fs(d), is_complex(i), n(i)
            f.write(struct.pack('ddii', t1, fs, 0, len(samples)))
            for s in samples:
                f.write(struct.pack('d', s))
        print("Zapisano.")

    def load_binary(self):
        fname = input("Plik do odczytu: ")
        try:
            with open(fname, 'rb') as f:
                h = f.read(24)
                t1, fs, _, n = struct.unpack('ddii', h)
                data = [struct.unpack('d', f.read(8))[0] for _ in range(n)]
                self.active_signal = DiscreteSignal(f"Plik:{fname}", 0, t1, 0, fs, samples=data)
                print(f"Wczytano {n} próbek.")
        except Exception as e:
            print(f"Błąd: {e}")

    def run(self):
        while True:
            act = self.active_signal.signal_type if self.active_signal else "Brak"
            print(f"\n--- AKTYWNY: {act} ---")
            print("1. Generuj | 2. Parametry | 3. Wykres | 4. Zapisz | 5. Odczyt | 0. Wyjście")
            c = input("Wybór: ")
            if c == '1':
                self.create_signal()
            elif c == '2' and self.active_signal:
                for k, v in self.active_signal.calculate_parameters().items(): print(f"{k}: {v:.4f}")
            elif c == '3' and self.active_signal:
                self.active_signal.draw_plot()
            elif c == '4':
                self.save_binary()
            elif c == '5':
                self.load_binary()
            elif c == '0':
                break


if __name__ == "__main__":
    SignalApp().run()