size = 5  # Rozmiar tablicy
# data_array = [None] * size  # Inicjalizacja tablicy z wartościami None
data_array = []  # Inicjalizacja tablicy z wartościami None

# # Wstawianie danych do wybranych indeksów
# data_array[1] = 'dane1'  # Wstawienie danych do indeksu 1
# data_array[4] = 'dane2'  # Wstawienie danych do indeksu 4


def dynamic_insert(data_list, index, data):
    # Rozszerzanie listy o 'None', jeśli indeks jest poza zakresem
    while index >= len(data_list):
        data_list.append(None)
    data_list[index] = data

dynamic_insert(data_array, 1, "dane1")
dynamic_insert(data_array, 4, "dane2")
print(data_array)  # Wyświetlenie tablicy
