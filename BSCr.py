from Receiverr import Receiver
import random
import asyncio

# Kanał BSC


class Channel:
    def __init__(self, counter, error_probability=0.001):
        self.receiver = Receiver(counter)
        self.counter = counter
        self.error_probability = error_probability

    async def transmit(self, frame):

        # wprowadza błędy do ramki z danymi
        frame = self.make_errors(frame)

        # wysyła do odbiornika i odbiera odpowiedź
        response = await self.receiver.receive_frame(frame)

        # wprowadza błędy do ramki ACK
        if (response):
            response = self.make_errors(response)

        return response

    def make_errors(self, data):
        """
        Symuluje kanał BSC, który ma określone prawdopodobieństwo zmiany bitu dla danych w formie bajtów.

        :param data: Dane w formie bajtów (typ bytes).
        :param error_probability: Prawdopodobieństwo zmiany bitu (odwrócenia 0 na 1 i odwrotnie).
        :return: Dane po przejściu przez kanał w formie bajtów.
        """
        def flip_bit(byte, bit_index):
            mask = 1 << bit_index
            return byte ^ mask

        modified_data = bytearray()
        for byte in data:
            modified_byte = byte
            for bit_index in range(8):
                if random.random() < self.error_probability:
                    modified_byte = flip_bit(modified_byte, bit_index)
            modified_data.append(modified_byte)

        if data != modified_data:
            print("        # wprowadza błędy do ramki ACK")
            # print(data)
            # print(len(modified_data))
            modified_data.append(1)
            # print(len(modified_data))
        else:
            modified_data.append(0)

        return bytearray(modified_data)
