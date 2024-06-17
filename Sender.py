import os
import hashlib
# import crcmod.predefined
from Counter import Counter
from BSC import Channel
import random
import asyncio
from colorama import Fore, Style
from FCS import FCS
from ChannelGilbertElliot import ChannelGilbertElliot

# Nadajnik


class Transmitter:
    def __init__(self, image_path, channel, counter, FCS_type):
        # obrazek
        self.image_path = image_path

        # kanał transmisyjny
        self.channel = channel

        # licznik ramek
        self.counter = counter

        # typ sumy kontrolnej
        # self.FCS_type = FCS.FCS_TYPE.PARITY_BIT.value
        # self.FCS_type = FCS.FCS_TYPE.CRC4.value
        # self.FCS_type = FCS.FCS_TYPE.CRC8.value
        # self.FCS_type = FCS.FCS_TYPE.HAMMING.value
        # self.FCS_type = FCS.FCS_TYPE.BCH.value
        self.FCS_type = FCS_type

        # rozmiar okna
        self.N = 7
        self.SN_min = 0
        self.SN_max = 0

        # rozmiary
        self.header_size = 4     # Rozmiar nagłówka w bajtach
        self.footer_size = 2     # Rozmiar sumy kontrolne kodów detekcyjnych i korkcyjnych

    # dzieli obrazek na kawałki
    def split_file(self):
        data_size = 200  # Przykładowy rozmiar danych
        parts = []

        with open(self.image_path, 'rb') as image_file:
            image_data = image_file.read()
            while image_data:
                frame_data = image_data[:data_size]
                image_data = image_data[data_size:]
                parts.append(frame_data)

        return parts

    # wysyła ramki
    async def send_frames(self):
        # dzieli obrazek
        frame_datas = self.split_file()
        # print(frame_datas[0])
        with open("dane.txt", "w") as file:
            file.write(b''.join(frame_datas).decode('utf-8', errors='replace'))


        # liczy liczbę ramek
        total_frames = len(frame_datas)

        print("total", total_frames)

        # wysyła ramki po N ramek bez ACK
        print("wysyłam od ", self.SN_max, " do ", self.SN_min + self.N)

        while self.SN_min < total_frames:

            # tworzy ramkę
            data = frame_datas[self.SN_max]

            # tworzy nagłówek
            is_end = self.SN_max == total_frames - 1

            header = self.create_header(
                self.SN_max, is_end, len(data), self.FCS_type)

            # składa ramkę
            frame = header + data

            # tworzy sumę kontrolną
            footer = FCS.encode(self.FCS_type, frame)

            # skłąda całą ramkę
            # print(type(frame), type(footer))
            full_frame = frame + footer

            await asyncio.sleep(0.01)
            # print(full_frame)
            # wysyła ramki bez czekania na ACK
            asyncio.create_task(self.send_frame(full_frame))

            print("wysłano: ", header[1])

            self.SN_max += 1

            # wysyła ponowanie ramki gdy wysłał wszystkie ramki z okna i nie dostał ACK
            if self.SN_max > self.SN_min + self.N:
                self.SN_max = self.SN_min
                print("wysyłam od nowa od ", self.SN_max,
                      " do ", self.SN_min + self.N)

            # wysyła ponownie ramki z okna gdy już nie ma więcej niewysłanych
            if self.SN_max == total_frames:
                self.SN_max = self.SN_min
                print("wysyłam od nowa od ", self.SN_max,
                      " do ", self.SN_min + self.N)

            # wysyła ramki z nowego okna po ACK
            if self.SN_min > self.SN_max:
                self.SN_max = self.SN_min
                print("wysyłam od nowa od ", self.SN_max,
                      " do ", self.SN_min + self.N)

    # wysyła ramkę

    async def send_frame(self, frame):

        # wysyła ramkę i czeka na odpowiedź
        response = await self.channel.transmit(frame)

        # zlicza wysłaną ramkę
        self.counter.inc_sent()

        # jeśli dostaje odpoweidź
        if response and response[1] > self.SN_min and response[1] < self.SN_min + self.N:
            is_error = response[-1]
            response = response[:-1]
            header, data, footer = self.extract_data(response)

            # checksum = FCS.decode(self.FCS_type, header)
            isCorrect, message = FCS.decode(self.FCS_type, response)

            # sprawdza czy nie ma błędów
            if not isCorrect:
                # zlicza błędną ramkę
                self.counter.inc_ack_error()
                return print("błąd w ack")

            if is_error and self.FCS_type != 4:
                print("                 NO TO ŁADNIE błąd przyjęty przez nadajnik")
                self.counter.inc_not_detected_ack()

            # zlicza poprawną ramkę
            self.counter.inc_ok()

            # przesuwa okno
            self.SN_min = response[1]

            print(Fore.GREEN + "Dostałem ack: ", self.SN_min-1,
                  "nowe okno", self.SN_min, "-", self.SN_min + self.N)
            if response[2]:
                print(Fore.GREEN + "Dostałem wszystkie ack (:")
            print(Style.RESET_ALL)

    # Tworzy nagłówek
    # header [rozmiar ramki, numer ramki, czy ostatnia ramka, typ FCS]
    # header [1B            ,1B         , 1B                , 1B]
    def create_header(self, frame_number, is_end, data_size, FCS_type):

        frame_size = data_size + self.footer_size  # Rozmiar ramki w bajtach

        header = bytearray([frame_size, frame_number, is_end, FCS_type])

        return header

    # dzieli ramkę na części

    def extract_data(self, frame):
        header = frame[:self.header_size]

        data = frame[self.header_size:-self.footer_size]  # Dane użytkownika

        footer = frame[-self.footer_size:]  # Stopka (sumy kontrolnej)

        return header, data, footer


# TESTY
image_path = "image.jpg"  # Ścieżka do obrazka
counter = Counter()


# Przykładowe wartości parametrów
p_good_to_bad = 0.01  # Prawdopodobieństwo przejścia z dobrego stanu do złego
p_bad_to_good = 0.1   # Prawdopodobieństwo przejścia ze złego stanu do dobrego
error_prob_good = 0.001  # Prawdopodobieństwo błędu w dobrym stanie
error_prob_bad = 0.1     # Prawdopodobieństwo błędu w złym stanie

# Przykładowe użycie
# channel = ChannelGilbertElliot(
#     counter, p_good_to_bad, p_bad_to_good, error_prob_good, error_prob_bad)
channel = Channel(counter, 0.0002)

# FCS_type = FCS.FCS_TYPE.PARITY_BIT.value
# FCS_type = FCS.FCS_TYPE.CRC4.value
# FCS_type = FCS.FCS_TYPE.CRC8.value
# FCS_type = FCS.FCS_TYPE.HAMMING.value
FCS_type = FCS.FCS_TYPE.BCH.value

transmitter = Transmitter(image_path, channel, counter, FCS_type)
asyncio.run(transmitter.send_frames())
counter.print_results()
