from enum import Enum
import bchlib
import hamming_codec


class FCS:
    # Definicja enuma dla dni tygodnia
    class FCS_TYPE(Enum):
        PARITY_BIT = 0
        CRC4 = 1
        CRC8 = 2
        HAMMING = 3
        BCH = 4

    @staticmethod
    # Funkcja wykonująca działanie zgodnie z wybranym typem kodowania
    def encode(FCS_type, message):
        switcher = {
            0: FCS.calculate_parity_bit(message),
            1: FCS.calculate_crc4(message),
            2: FCS.calculate_crc8(message),
            # 3: "Wybrano kodowanie Hamminga",
            3: FCS.calculate_crc16(message),
            4: FCS.calculate_bch(message)
        }
        # return switcher.get(FCS_type, "Niepoprawny typ kodowania")
        return switcher.get(FCS_type, 0b00)

    @staticmethod
    # Funkcja wykonująca działanie zgodnie z wybranym typem kodowania
    def decode(FCS_type, frame):
        message, footer = frame[:-2], frame[-2:]
        bch_copy = message[:]
        switcher = {
            0: [FCS.compare_bits(FCS.calculate_parity_bit(message), footer, 1), message],
            1: [FCS.compare_bits(FCS.calculate_crc4(message), footer, 4), message],
            2: [FCS.compare_bits(FCS.calculate_crc8(message), footer, 8), message],
            3: [FCS.compare_bits(FCS.calculate_crc16(message), footer, 16), message],
            4: FCS.decode_bch(bch_copy, footer)
        }
        return switcher.get(FCS_type, [False, message])

    @staticmethod
    def calculate_parity_bit(message):
        # Oblicz sumę modulo 2 na wszystkich bitach wiadomości
        parity_bit = sum(bin(byte).count("1") for byte in message) % 2

        return parity_bit.to_bytes(2,"big")

    @staticmethod
    def calculate_crc4(message):
        """
        Oblicza CRC-4 dla podanych danych w formie bajtów.

        :param data: Dane w formie bajtów (typ bytes).
        :return: CRC-4 jako 4-bitowa wartość (typ int).
        """
        # Używamy wielomianu CRC-4: x^4 + x + 1 (czyli 0b0011)
        polynomial = 0b0011
        crc = 0

        # Przechodzimy przez każdy bajt w danych
        for byte in message:
            # Przechodzimy przez każdy bit w bajcie
            for i in range(8):
                bit = (byte >> (7 - i)) & 1
                # Przesunięcie CRC w lewo i dodanie nowego bitu
                crc = ((crc << 1) | bit) & 0b1111

                if crc & 0b10000:  # Jeśli najwyższy bit jest ustawiony
                    crc ^= polynomial  # Wykonujemy operację XOR z wielomianem

        # Zwracamy ostatnie 4 bity CRC
        return crc.to_bytes(2,"big")

    @staticmethod
    def calculate_crc8(message):
        """
        Oblicza CRC-8 dla podanych danych w formie bajtów.

        :param message: Dane w formie bajtów (typ bytes).
        :return: CRC-8 jako 8-bitowa wartość (typ int).
        """
        # Używamy wielomianu CRC-8: x^8 + x^2 + x + 1 (czyli 0b00000111)
        polynomial = 0b00000111
        crc = 0

        # Przechodzimy przez każdy bajt w danych
        for byte in message:
            # Przechodzimy przez każdy bit w bajcie
            for i in range(8):
                bit = (byte >> (7 - i)) & 1
                # Przesunięcie CRC w lewo i dodanie nowego bitu
                crc = ((crc << 1) | bit) & 0xFF

                if crc & 0x100:  # Jeśli najwyższy bit jest ustawiony
                    crc ^= polynomial  # Wykonujemy operację XOR z wielomianem

        # Zwracamy ostatnie 8 bitów CRC
        return crc.to_bytes(2,"big")

    @staticmethod
    def calculate_crc16(message):
        """
        Oblicza CRC-16 dla podanych danych w formie bajtów.

        :param message: Dane w formie bajtów (typ bytes).
        :return: CRC-16 jako 16-bitowa wartość (typ int).
        """
        # Używamy wielomianu CRC-16: x^16 + x^15 + x^2 + 1 (czyli 0b11000000000000101)
        polynomial = 0b11000000000000101
        crc = 0xFFFF  # Początkowe CRC (wszystkie bity ustawione na 1)

        # Przechodzimy przez każdy bajt w danych
        for byte in message:
            crc ^= byte << 8  # XOR z górnymi 8 bitami CRC

            for _ in range(8):  # Przechodzimy przez każdy bit w bajcie
                if crc & 0x8000:  # Jeśli najwyższy bit jest ustawiony
                    # Przesunięcie w lewo i XOR z polinomem
                    crc = (crc << 1) ^ polynomial
                else:
                    crc = crc << 1  # Przesunięcie w lewo

                crc &= 0xFFFF  # Zabezpieczenie, aby CRC pozostało 16-bitowe

        return crc.to_bytes(2,"big")

    @staticmethod
    def calculate_bch(message):

        bch = bchlib.BCH(1, m=11)  # correct 1 error, n = 2^m-1 = 2047 bits

        max_data_len = bch.n // 8 - (bch.ecc_bits + 7) // 8

        data = message+bytearray("0"*(max_data_len-len(message)), 'utf-8')

        return bch.encode(data)

    @staticmethod
    def decode_bch(message, ecc):

        # decode
        bch = bchlib.BCH(1, m=11)  # correct 1 error, n = 2^m-1 = 2047 bits

        # bch.data_len = max_data_len
        nerr = bch.decode(message, ecc)

        print('nerr:', nerr)

        if nerr <= bch.t:

            bch.correct(message, ecc)
            return True, message
        else:
            return False, message

    @staticmethod
    def calculate_hamming(message):
        """
        Zakodowanie wiadomości przy użyciu kodu Hamminga.

        Parameters:
        message (str): Wiadomość do zakodowania.

        Returns:
        str: Zakodowana wiadomość.
        """
        # Konwersja wiadomości do formatu int
        message_int = int.from_bytes(message.encode(), 'big')
        n_bits = len(message) * 8

        # Kodowanie Hamminga
        encoded_message = hamming_codec.encode(message_int, n_bits)
        
        return encoded_message

    @staticmethod
    def decode_hamming(encoded_message):
        """
        Dekodowanie wiadomości przy użyciu kodu Hamminga i poprawianie błędów.

        Parameters:
        encoded_message (str): Zakodowana wiadomość.

        Returns:
        tuple: (bool, str) - Flaga powodzenia oraz odkodowana wiadomość.
        """
        # Konwersja zakodowanej wiadomości na int
        encoded_message_int = int(encoded_message, 2)

        # Dekodowanie Hamminga
        decoded_message_bin = hamming_codec.decode(encoded_message_int, len(encoded_message))
        decoded_message_int = int(decoded_message_bin, 2)
        
        # Konwersja z powrotem na str
        try:
            decoded_message = decoded_message_int.to_bytes((decoded_message_int.bit_length() + 7) // 8, 'big').decode()
            return True, decoded_message
        except Exception as e:
            print(f"Decoding error: {e}")
            return False, ""

    @staticmethod
    def compare_bits(message1, message2, n_bits, from_end=True):
        """
        Porównuje n ostatnich lub pierwszych bitów wiadomości.

        Parameters:
        message1 (bytes): Pierwsza wiadomość.
        message2 (bytes): Druga wiadomość.
        n_bits (int): Liczba bitów do porównania.
        from_end (bool): Czy porównywać od końca wiadomości. Domyślnie True.

        Returns:
        bool: True, jeśli bity są takie same, False w przeciwnym razie.
        """
        # Konwersja wiadomości na bity
        bits1 = ''.join(format(byte, '08b') for byte in message1)
        bits2 = ''.join(format(byte, '08b') for byte in message2)

        if from_end:
            return bits1[-n_bits:] == bits2[-n_bits:]
        else:
            return bits1[:n_bits] == bits2[:n_bits]