import struct
import math


# --- TYMCZASOWE ZAŚLEPKI (To dostarczy kolega) ---
class Signal:
    def __init__(self, name="Testowy", samples=None, fs=1.0, t0=0.0):
        self.name = name
        self.samples = samples if samples else [0.0] * 100
        self.fs = fs
        self.t0 = t0
        self.is_complex = 0

    def calculate_params(self):
        # Symulacja obliczeń z punktu 2
        return {"Mean": 0.5, "RMS": 0.707, "Variance": 0.25}


# --- TWOJA LOGIKA MENU I OPERACJI ---
class SignalApp:
    def __init__(self):
        self.active_signal = None
        self.buffer_signal = None

    def save_binary(self, signal, filename):
        """Implementacja punktu 3 - zapis binarny (double precision)"""
        try:
            with open(filename, 'wb') as f:
                # Nagłówek: t0 (d), fs (d), is_complex (i), n_samples (i)
                header = struct.pack('ddii', signal.t0, signal.fs, signal.is_complex, len(signal.samples))
                f.write(header)
                # Dane: amplitudy (double)
                for s in signal.samples:
                    f.write(struct.pack('d', s))
            print(f"Poprawnie zapisano do: {filename}")
        except Exception as e:
            print(f"Błąd zapisu: {e}")

    def load_binary(self, filename):
        """Implementacja punktu 3 - odczyt binarny"""
        try:
            with open(filename, 'rb') as f:
                header_data = f.read(24)  # 8+8+4+4 bajty
                t0, fs, is_complex, n = struct.unpack('ddii', header_data)
                samples = []
                for _ in range(n):
                    sample = struct.unpack('d', f.read(8))[0]
                    samples.append(sample)
                return Signal(name=filename, samples=samples, fs=fs, t0=t0)
        except Exception as e:
            print(f"Błąd odczytu: {e}")
            return None

    def run(self):
        while True:
            print(f"\n--- AKTYWNY: {self.active_signal.name if self.active_signal else 'Brak'} ---")
            print("1. Generuj (testowy)")
            print("2. Zapisz aktywny")
            print("3. Wczytaj do bufora")
            print("4. Wykonaj operację (Aktywny + Bufor)")
            print("0. Wyjście")

            choice = input("Wybierz: ")

            if choice == '1':
                self.active_signal = Signal("Wygenerowany", [math.sin(x / 10) for x in range(100)])
                print("Sygnał wygenerowany!")
            elif choice == '2':
                if self.active_signal:
                    self.save_binary(self.active_signal, "signal.bin")
                else:
                    print("Brak sygnału!")
            elif choice == '3':
                self.buffer_signal = self.load_binary("signal.bin")
                if self.buffer_signal: print("Wczytano do bufora.")
            elif choice == '4':
                if self.active_signal and self.buffer_signal:
                    # Automatyczny zapis po operacji (Punkt 4)
                    new_samples = [a + b for a, b in zip(self.active_signal.samples, self.buffer_signal.samples)]
                    self.active_signal = Signal("Wynik", new_samples)
                    self.save_binary(self.active_signal, "wynik_operacji.bin")
                    print("Operacja wykonana i zapisana.")
            elif choice == '0':
                break


if __name__ == "__main__":
    app = SignalApp()
    app.run()