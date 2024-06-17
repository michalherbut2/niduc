from Receiver import Receiver
import random
import asyncio


class ChannelGilbertElliot:
    def __init__(self, counter, p_good_to_bad, p_bad_to_good, error_prob_good, error_prob_bad):
        self.receiver = Receiver(counter)
        self.counter = counter
        # Prawdopodobieństwo przejścia z dobrego stanu do złego
        self.p_good_to_bad = p_good_to_bad
        # Prawdopodobieństwo przejścia ze złego stanu do dobrego
        self.p_bad_to_good = p_bad_to_good
        # Prawdopodobieństwo błędu w dobrym stanie
        self.error_prob_good = error_prob_good
        self.error_prob_bad = error_prob_bad  # Prawdopodobieństwo błędu w złym stanie
        self.is_good_state = True  # Zaczynamy w dobrym stanie

    async def transmit(self, frame):
        # Wprowadza błędy do ramki z danymi
        frame = self.make_errors(frame)

        # Wysyła do odbiornika i odbiera odpowiedź
        response = await self.receiver.receive_frame(frame)

        # Wprowadza błędy do ramki ACK
        if response:
            response = self.make_errors(response)

        return response

    def make_errors(self, data):
        """
        Symuluje kanał Gilbert-Elliot, który przełącza się między dwoma stanami:
        dobrym i złym, wprowadzając błędy do danych w formie bajtów.

        :param data: Dane w formie bajtów (typ bytes).
        :return: Dane po przejściu przez kanał w formie bajtów.
        """
        def flip_bit(byte, bit_index):
            mask = 1 << bit_index
            return byte ^ mask

        modified_data = bytearray()
        for byte in data:
            modified_byte = byte
            for bit_index in range(8):
                if self.is_good_state:
                    error_probability = self.error_prob_good
                else:
                    error_probability = self.error_prob_bad

                if random.random() < error_probability:
                    modified_byte = flip_bit(modified_byte, bit_index)

            modified_data.append(modified_byte)

        # Przełączenie stanu
        if self.is_good_state:
            if random.random() < self.p_good_to_bad:
                self.is_good_state = False
        else:
            if random.random() < self.p_bad_to_good:
                self.is_good_state = True

        if data != modified_data:
            print("        # wprowadza błędy do ramki ACK")
            # print(data)
            # print(len(modified_data))
            modified_data.append(1)
            # print(len(modified_data))
        else:
            modified_data.append(0)

        return bytearray(modified_data)
