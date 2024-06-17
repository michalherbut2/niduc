import os
import hashlib
# import crcmod.predefined
from Receiver import Receiver
from BSC import Channel
import random
import asyncio


class Transmitter:
    def __init__(self, image_path, channel):
        self.image_path = image_path
        self.channel = channel

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

    def send_frames(self):
        frame_datas = self.split_file()
        total_frames = len(frame_datas)

        for i, data in enumerate(frame_datas):
            header = self.create_header(i, total_frames, len(data))

            frame = header + data

            # footer = self.calculate_checksum(frame)
            footer = self.calculate_parity_bit(frame)
            print("footer", footer, "\n")

            full_frame = frame + footer

            response = self.channel.transmit(full_frame)
            print("response", response)

            while (response[-1] == 1):
                response = self.channel.transmit(full_frame)
                print("ponowna odpowiedz", response)

        return 0

    async def send_frame(self, frame):

        # response = await self.channel.transmit(frame)
        # print("response",response)

        # while (response[-1] == 1):
        #     response = self.channel.transmit(frame)
        #     print("ponowna odpowiedz",response)

        try:
            response = await asyncio.wait_for(self.channel.transmit(frame), timeout=2)
            print("response", response)

        except asyncio.TimeoutError:
            print("Przekroczono limit czasu (2 sekundy) dla zadania.")

        return 0

    # header [rozmiar ramki, numer ramki, czy ostatnia ramka/liczba wszystkich ramek, unikalny identyfikator]
    # header [1B            ,1B                 , 1B                                        , 1B]
    def create_header(self, frame_number, total_frames, data_size):
        # rozmiary
        header_size = 4     # Rozmiar nagłówka w bajtach
        footer_size = 2     # Rozmiar sumy kontrolne kodów detekcyjnych i korkcyjnych

        frame_size = header_size + data_size + footer_size  # Rozmiar ramki w bajtach

        # header = bytearray([frame_size, frame_number & 0x0F, int(frame_number == total_frames), frame_number >> 4])
        header = bytearray(
            [frame_size, frame_number, total_frames, frame_number])
        # header = (frame_size).to_bytes(1, byteorder='big') + bytearray([frame_number, total_frames, frame_number])

        print("header", header)
        return header

    def calculate_parity_bit(self, message):
        # Oblicz sumę modulo 2 na wszystkich bitach wiadomości
        parity_bit = sum(int(bit) for bit in message) % 2
        print("bit parzystosci ", parity_bit)
        if (parity_bit):
            return b'\x00\x01'
        else:
            return b'\x00\x00'

    def calculate_checksum(self, data):
        # Utwórz obiekt CRC32
        # crc32 = crcmod.mkCrcFun(0x104c11db7, initCrc=0, xorOut=0xFFFFFFFF)
        # crc32 = crcmod.mkCrcFun(0x104c11db7)
        # crc32 = crcmod.predefined.mkPredefinedCrcFun('crc-32')
        # crc_value = bytearray(crc32(data))
        crc_value = hashlib.md5(data).digest()
        # print(checksum)
        return crc_value


image_path = "image.jpg"  # Ścieżka do obrazka
transmitter = Transmitter(image_path, Channel())
sent_frames = transmitter.send_frames()
# print(sent_frames[0])
# print(len(sent_frames))
