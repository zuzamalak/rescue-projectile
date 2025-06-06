import math
import matplotlib.pyplot as plt

def input_positive_float(prompt):
    """
    Pobiera od użytkownika dodatnią liczbę zmiennoprzecinkową.
    W razie niepoprawnego formatu lub wartości <=0 prosi ponownie.
    """
    while True:
        try:
            # Wyświetla prompt i konwertuje wejście na float
            value = float(input(prompt))
            # Sprawdza, czy liczba jest większa od zera
            if value <= 0:
                print("Błąd: wartość musi być liczbą dodatnią (> 0).")
                # Jeśli warunek nie jest spełniony, powtarza pętlę
                continue
            # Zwraca poprawnie wczytaną dodatnią wartość
            return value
        except ValueError:
            # Jeśli konwersja się nie powiedzie, informuje użytkownika i powtarza pętlę
            print("Błąd: proszę podać liczbę.")


def calculate_horizontal_velocity(l, H, g=9.81):
    """
    Oblicza prędkość poziomą v_x potrzebną, 
    żeby rzutka z wysokości H pokonała odległość l (wyrzut poziomy).
    v_x = l / sqrt(2H/g)
    """
    # Oblicza czas opadania z wysokości H: t = sqrt(2·H/g)
    t = math.sqrt(2 * H / g)
    # Prędkość poziomą liczy jako odległość l podzieloną przez czas lotu t
    return l / t

def calculate_launch_angles(v0, l, H, g=9.81):
    """
    Oblicza możliwe kąty wyrzutu (w stopniach) dla początkowej prędkości v0,
    odległości l i wysokości wyrzutu H przy przyspieszeniu g.
    Zwraca listę kątów [α1, α2] posortowaną rosnąco, lub [] jeśli brak rozwiązania.
    """
    # współczynniki równania kwadratowego dla T = tan(α)
    # a·T² + b·T + c = 0
    a = (g * l**2) / (2 * v0**2)
    b = -l
    c = a - H

    # oblicza wyróżnik (delta) równania kwadratowego
    disc = b**2 - 4 * a * c
    if disc < 0:
        # jeśli delta < 0, brak rzeczywistych rozwiązań. Zwraca pustą listę
        return []

    # pierwiastek wyróżnika
    sqrt_disc = math.sqrt(disc)

    # dwa rozwiązania równania kwadratowego dla tan(α)
    tan1 = (-b + sqrt_disc) / (2 * a)
    tan2 = (-b - sqrt_disc) / (2 * a)

    angles = []
    # filtruje tylko dodatnie wartości tan(α), bo kąt wyrzutu musi być dodatni
    for t in (tan1, tan2):
        if t > 0:
            # zamiana tangensa na kąt w stopniach
            angles.append(math.degrees(math.atan(t)))

    # zwraca posortowaną listę możliwych kątów
    return sorted(angles)

def plot_angles_for_bodies(v0, l, H):
    """
    Rysuje wykres słupkowy kątów wyrzutu dla ciał niebieskich (Merkury, Ziemia, Księżyc, Mars, Ganimedes, Ceres)
    przy podanych v0, l, H. Dane zostały pozyskane z wikipedii.
    Wikipedia – sekcje „Physical characteristics” / „Surface gravity”
        Merkury: https://en.wikipedia.org/wiki/Mercury_(planet)#Physical_characteristics
        Ziemia: https://en.wikipedia.org/wiki/Earth#Physical_characteristics
        Księżyc: https://en.wikipedia.org/wiki/Moon#Physical_characteristics
        Mars: https://en.wikipedia.org/wiki/Mars#Physical_characteristics
        Ganimedes: https://en.wikipedia.org/wiki/Ganymede_(moon)#Physical_characteristics
        Ceres: https://en.wikipedia.org/wiki/Ceres_(dwarf_planet)#Physical_characteristics
    """
    # Dane ciał niebieskich i ich przyspieszeń grawitacyjnych [m/s²]
    bodies = {
        "Merkury": 3.70,
        "Ziemia": 9.81,
        "Księżyc": 1.62,
        "Mars": 3.71,
        "Ganimedes": 1.425,
        "Ceres": 0.27
    }

    names = []  # lista nazw ciał do osi X
    vals = []   # lista kątów do osi Y

    # Dla każdego ciała wylicza najniższy możliwy kąt wyrzutu
    for name, g in bodies.items():
        ang = calculate_launch_angles(v0, l, H, g)  # możliwe kąty przy danym g
        alpha = ang[0] if ang else None               # bierze najmniejszy kąt lub None, gdy brak rozwiązania
        names.append(name)                             # dodaje nazwę ciała
        # jeśli kąt jest None, zastępuje wartością 0 (wykres będzie miał pusty słupek)
        vals.append(alpha if alpha is not None else 0)

    # Tworzy wykres słupkowy
    plt.figure()
    bars = plt.bar(names, vals)                        # rysuje słupki: name→val
    plt.ylabel("Kąt wyrzutu [°]")                       # etykieta osi Y
    plt.title("Kąt wyrzutu dla różnych ciał niebieskich")  # tytuł wykresu
    plt.xticks(rotation=45)                             # obrót etykiet na osi X dla czytelności

    # Dodaje wartość nad każdym słupkiem
    for bar, alpha in zip(bars, vals):
        # jeśli alfa > 0, wyświetla wartość z jedną cyfrą po przecinku, w przeciwnym razie kreskę
        label = f"{alpha:.1f}°" if alpha > 0 else "–"
        # pozycjonuje tekst: na środku słupka, nieco powyżej jego wysokości
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.1,
            label,
            ha='center', va='bottom'
        )

    plt.tight_layout()  # automatycznie poprawia marginesy, by etykiety się nie nakładały
    plt.show()          # wyświetla wynikowy wykres

def main():
    while True:
        # Wyświetla główne menu programu
        print("\n=== Rzutka ratunkowa – kalkulator ===")
        print("1) Oblicz prędkość poziomą v_x")
        print("2) Oblicz kąt wyrzutu α")
        print("3) Wykres kątów dla różnych ciał niebieskich")
        print("0) Wyjście")
        choice = input("Wybierz opcję: ")
        
        choice = choice.strip()  # usunięcie zbędnych spacji/enterów
        
        if choice == "1":
            # Opcja 1: obliczenie prędkości poziomej v_x
            l = input_positive_float("Podaj odległość l [m]: ")   # pobiera odległość
            H = input_positive_float("Podaj wysokość H [m]: ")    # pobiera wysokość
            vx = calculate_horizontal_velocity(l, H)              # liczy v_x
            print(f"\nWymagana prędkość pozioma: {vx:.2f} m/s")   # wyświetla wynik
        
        elif choice == "2":
            # Opcja 2: obliczenie możliwych kątów wyrzutu α
            v0 = input_positive_float("Podaj prędkość początkową v0 [m/s]: ")  # pobiera v0
            l  = input_positive_float("Podaj odległość l [m]: ")               # pobiera odległość
            H  = input_positive_float("Podaj wysokość H [m]: ")                # pobiera wysokość
            angles = calculate_launch_angles(v0, l, H)                        # liczy kąty
            if not angles:
                # brak rozwiązania – nieosiągalne przy podanych danych
                print("\nBrak rozwiązania – nieosiągalne przy podanych danych.")
            else:
                # wyświetla wszystkie możliwe kąty
                print("\nMożliwe kąty wyrzutu:")
                for a in angles:
                    print(f"     {a:.2f}°")
        
        elif choice == "3":
            # Opcja 3: rysuje wykres kątów dla różnych ciał niebieskich
            v0 = input_positive_float("Podaj prędkość początkową v0 [m/s]: ")
            l  = input_positive_float("Podaj odległość l [m]: ")
            H  = input_positive_float("Podaj wysokość H [m]: ")
            plot_angles_for_bodies(v0, l, H)  # tworzy i wyświetla wykres
        
        elif choice == "0":
            # Wyjście z programu
            print("Koniec programu.")
            break  # przerywa pętlę główną
        
        else:
            # Obsługa nieprawidłowej opcji
            print("Nieprawidłowy wybór. Spróbuj ponownie.")

if __name__ == "__main__":
    # Punkt wejścia do programu
    main()
