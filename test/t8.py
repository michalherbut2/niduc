def hamming_encode(message):
    n = 1023
    k = 1013
    parity_bits = n - k

    # Dodaj bity parzystości na odpowiednich pozycjach
    j = 0
    l = 1
    encoded = ""
    for i in range(1, n + 1):
        if i == 2**j:
            encoded += '0'
            j += 1
        else:
            if l <= len(message):
                encoded += message[l-1]
                l += 1
            else:
                encoded += '0'

    # Oblicz wartości bitów parzystości
    for i in range(parity_bits):
        val = 0
        for j in range(1, n + 1):
            if j & (2**i) != 0:  # Sprawdź, czy bit parzystości jest ustawiony
                val ^= int(encoded[-j])  # XOR operacja

        # Ustaw wartość bitu parzystości na obliczoną wartość
        encoded = encoded[:n - (2**i)] + str(val) + encoded[n - (2**i) + 1:]

    return encoded

# Przykładowe użycie
message = '1' * 1000  # Twoja wiadomość powinna mieć długość 1000 bitów
encoded = hamming_encode(message)
print('Zakodowana wiadomość:', encoded)


def hamming_decode(encoded):
    n = 1023
    k = 1013
    parity_bits = n - k

    # Oblicz wartości bitów parzystości
    for i in range(parity_bits):
        val = 0
        for j in range(1, n + 1):
            if j & (2**i) != 0:  # Sprawdź, czy bit parzystości jest ustawiony
                val ^= int(encoded[-j])  # XOR operacja

        # Sprawdź, czy wartość bitu parzystości jest poprawna
        if val != int(encoded[-(2**i)]):
            print('Błąd wykryty na pozycji', 2**i)
            return None  # Zwróć None, jeśli wykryto błąd

    # Usuń bity parzystości, aby uzyskać oryginalną wiadomość
    j = 0
    decoded = ""
    for i in range(1, n + 1):
        if i != 2**j:
            decoded += encoded[-i]
        else:
            j += 1

    return decoded

# Przykładowe użycie
#encoded = '1' * 1023  # Twoja zakodowana wiadomość powinna mieć długość 1023 bity
decoded = hamming_decode(encoded)
if decoded is not None:
    print('Zdekodowana wiadomość:', decoded)
else:
    print('Nie można zdekodować wiadomości z powodu wykrytych błędów')
