import hamming_codec

# Dane wejściowe
input_data = 0x4235
n_bits = 16

# Kodowanie Hamminga
encoded_message = hamming_codec.encode(input_data, n_bits)
print("Encoded message:", encoded_message)

# Konwersja zakodowanej wiadomości na szesnastkowy format
encoded_message_hex = hex(int(encoded_message, 2))
print("Encoded message (hex):", encoded_message_hex)

# Wprowadzenie błędu (na przykładzie zamiany pierwszego bitu)
corrupted_message = list(encoded_message)
corrupted_message[0] = '1' if corrupted_message[0] == '0' else '0'
corrupted_message = ''.join(corrupted_message)
print("Corrupted message:", corrupted_message)

# Dekodowanie Hamminga
decoded_message = hamming_codec.decode(int(corrupted_message, 2), len(corrupted_message))
print("Decoded message:", decoded_message)

# Konwersja odkodowanej wiadomości na szesnastkowy format
decoded_message_hex = hex(int(decoded_message, 2))
print("Decoded message (hex):", decoded_message_hex)
