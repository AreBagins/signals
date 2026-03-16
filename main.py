import struct
import math
import numpy as np
from signals import Signal, ContinousSignal, DiscreteSignal

# --- TWOJA LOGIKA MENU I OPERACJI ---
class SignalApp:
    def __init__(self):
        self.active_signal = None
        self.buffer_signal = None
    
    def create_test_signal(self):
    #Tworzy testowy sygnał dyskretny
        print("\n--- GENEROWANIE SYGNAŁU TESTOWEGO ---")
        print("1. Sygnał ciągły (zostanie zdyskretyzowany)")
        print("2. Sygnał dyskretny")
        choice = input("Wybierz typ: ")

        if choice == '1':
            # Tworzenie sygnału ciągłego
            signal_type = input("Typ sygnału (sin/prostokat/piła): ")
            # W zależności od typu wyświetlamy potrzebne parametry do wypełnienia
            # Na razie tego nie ma
            print("\nParametry sygnału ciągłego:")
            A = float(input("Amplituda: "))
            t1 = float(input("Czas początkowy: "))
            d = float(input("Czas trwania: "))
            T = float(input("Okres: "))
            k = float(input("Wypełnienie: "))
            ts = float(input("Czas skoku: "))
            
            print("Sygnał ciągły utworzony.")
            
        elif choice == '2':
            # Tworzenie sygnału dyskretnego
            print("\nParametry sygnału dyskretnego:")
            signal_type = input("Typ sygnału (sin/prostokat/szum): ")
            # W zależności od typu wyświetlamy potrzebne parametry do wypełnienia
            # Na razie tego nie ma
            A = float(input("Amplituda: "))
            n1 = int(input("Numer pierwszej próbki: "))
            t1 = float(input("Czas początkowy: "))
            ns = int(input("Próbka skoku: "))
            f = float(input("Częstotliwość próbkowania: "))
            d = float(input("Czas trwania: "))
            p = float(input("Prawdopodobieństwo: "))
            
        print("Sygnał testowy wygenerowany!")

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
    def perform_operation(self, operation):
        print("Operacja dokonana")

    def run(self):
        while True:
            print("\n" + "="*50)
            active_name = self.active_signal.signal_type if self.active_signal else 'Brak'
            buffer_name = self.buffer_signal.signal_type if self.buffer_signal else 'Brak'
            print(f"AKTYWNY: {active_name} | BUFOR: {buffer_name}")
            print("="*50)
            print("1. Generuj sygnał testowy")
            print("2. Wyświetl informacje o sygnale aktywnym")
            print("3. Wyświetl informacje o buforze")
            print("4. Zapisz aktywny sygnał do pliku")
            print("5. Wczytaj sygnał z pliku do bufora")
            print("6. Wykonaj operację (Aktywny + Bufor)")
            print("7. Rysuj wykres sygnału aktywnego")
            print("8. Rysuj histogram sygnału aktywnego")
            print("9. Oblicz parametry sygnału aktywnego")
            print("10. Przenieś bufor do aktywnego")
            print("0. Wyjście")

            choice = input("\nWybierz opcję: ")

            if choice == '1':
                self.create_test_signal()

            elif choice == '2':
                self.display_signal_info(self.active_signal, "Aktywny")

            elif choice == '3':
                self.display_signal_info(self.buffer_signal, "Bufor")

            elif choice == '4':
                if self.active_signal:
                    filename = input("Podaj nazwę pliku (np. signal.bin): ")
                    self.save_binary(self.active_signal, filename)
                else:
                    print("Brak aktywnego sygnału!")

            elif choice == '5':
                filename = input("Podaj nazwę pliku do wczytania: ")
                self.buffer_signal = self.load_binary(filename)
                if self.buffer_signal:
                    print("Wczytano do bufora.")

            elif choice == '6':
                if self.active_signal and self.buffer_signal:
                    print("\nDostępne operacje: + (dodawanie), - (odejmowanie), * (mnożenie), / (dzielenie)")
                    op = input("Wybierz operację: ")
                    self.perform_operation(op)
                else:
                    print("Brak wymaganych sygnałów!")

            elif choice == '7':
                if self.active_signal:
                    self.active_signal.draw_plot()
                else:
                    print("Brak aktywnego sygnału!")

            elif choice == '8':
                if self.active_signal:
                    try:
                        range_val = float(input("Podaj zakres histogramu: "))
                        self.active_signal.draw_histogram(range_val)
                    except ValueError:
                        print("Podaj poprawną liczbę!")
                else:
                    print("Brak aktywnego sygnału!")

            elif choice == '9':
                if self.active_signal:
                    result = self.active_signal.calculate_parameters()
                    print(f"Wynik obliczeń parametrów: {result}")
                else:
                    print("Brak aktywnego sygnału!")

            elif choice == '10':
                if self.buffer_signal:
                    self.active_signal = self.buffer_signal
                    self.buffer_signal = None
                    print("Przeniesiono bufor do aktywnego sygnału.")
                else:
                    print("Bufor jest pusty!")

            elif choice == '0':
                print("Do widzenia!")
                break

            else:
                print("Nieprawidłowy wybór!")


if __name__ == "__main__":
    app = SignalApp()
    app.run()