import hashlib

class RamkaDanych:
    def __init__(self, rozmiar, numer_sekwencyjny, ostatnia_ramka, id_ramki, dane_uzytkownika):
        self.rozmiar = rozmiar
        self.numer_sekwencyjny = numer_sekwencyjny
        self.ostatnia_ramka = ostatnia_ramka
        self.id_ramki = id_ramki
        self.dane_uzytkownika = dane_uzytkownika

    def oblicz_crc16(self):
        # Symulacja obliczenia sumy kontrolnej CRC16
        return hashlib.md5(self.dane_uzytkownika.encode()).hexdigest()

class RamkaPotwierdzenia:
    def __init__(self, numer_potwierdzonej_ramki, potwierdzenie, zadanie_powtorzenia):
        self.numer_potwierdzonej_ramki = numer_potwierdzonej_ramki
        self.potwierdzenie = potwierdzenie
        self.zadanie_powtorzenia = zadanie_powtorzenia

    def oblicz_crc8(self):
        # Symulacja obliczenia sumy kontrolnej CRC8
        return hashlib.md5(str(self.numer_potwierdzonej_ramki).encode()).hexdigest()

# Przykładowe użycie
ramka_danych = RamkaDanych(1024, 1, True, 123, "Dane użytkownika...")
print("Suma kontrolna CRC16:", ramka_danych.oblicz_crc16())

ramka_potwierdzenia = RamkaPotwierdzenia(1, True, False)
print("Suma kontrolna CRC8:", ramka_potwierdzenia.oblicz_crc8())
