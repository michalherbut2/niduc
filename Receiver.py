import hashlib
# import crcmod
import io
from PIL import Image
import asyncio
from FCS import FCS

# Odbiornik


class Receiver:
    def __init__(self, counter):
        # licznik ramek
        self.counter = counter

        # numer oczekiwanej ramki
        self.RN = 0

        # przechowuje odebrany obrazek
        self.data_buffer = b''

        # typ kodu detekcyjnego/korekcyjnego
        # self.FCS_type = FCS.FCS_TYPE.PARITY_BIT

        # rozmiary
        self.header_size = 4     # Rozmiar nagłówka w bajtach
        self.footer_size = 2     # Rozmiar sumy kontrolne kodów detekcyjnych i korkcyjnych

    # odbiera ramkę z danymi

    async def receive_frame(self, frame):
        # rozdziela ramkę na części
        # print(len(frame))
        is_error = frame[-1]
        frame = frame[:-1]
        # print(len(frame))
        header, data, footer = self.extract_data(frame)

        # rozdziela nagłówek na części
        frame_size, frame_number, is_end, FCS_type = header

        self.FCS_type = FCS_type

        # oblicza sumę kontrolną
        decoded=FCS.decode(self.FCS_type, frame)
        if len(decoded) >2:
            print("XXXXXXXXXXxxx")
            print(decoded)
        isCorrect, message = decoded
        header, data = message[:4], message[4:]
        # print(message)
        # print(header)
        # print(data)
        # print(len(message))
        # print(len(header))
        # print(len(data))

        frame_size, frame_number, is_end, FCS_type = header

        # odrzuca niekolejne ramki
        if frame_number != self.RN:
            self.counter.inc_out_of_order()
            print(
                f"Received out-of-order frame {frame_number}. Ignoring. Expected {self.RN}")
            return False

        # odrzuca uszkodzone ramki
        if not isCorrect:
            self.counter.inc_error()
            print(f"Received frame {frame_number} with incorrect checksum. Requesting retransmission.")
            return False

        # akceptuje kolejną ramkę
        if frame_number == self.RN:
            if is_error and self.FCS_type != 4:
                print("                 NO TO ŁADNIE")
                self.counter.inc_not_detected()
            # dodaje dane do burofa
            # print("self.data_buffer",self.data_buffer)
            self.data_buffer += data
            # print("self.data_buffer",self.data_buffer)
            # sprawdza czy ostatnia
            if header[2]:
                # zapisuje obrazek
                print("ZAPISUJE OBRAZ:::")
                try:
                    image = Image.open(io.BytesIO(self.data_buffer))
                    image.save("out.jpg")
                    
                except Exception as e:
                    # Jeśli wystąpił błąd, wyświetlamy komunikat o błędzie
                    print(f"An error occurred: {e}")
   
                with open("out.txt", "w") as file:
                    file.write(self.data_buffer.decode('utf-8', errors='replace'))

                print("Obrazek został zapisany w folderze:", "obrazek.jpg")

            # wysyła ACK z numerem kolejnej oczekiwanej ramki
            self.RN += 1
            return self.send_ack(self.RN, is_end, frame_number)

    # rozdziela nagłówek na częsci

    def extract_data(self, frame):
        header = frame[:self.header_size]

        data = frame[self.header_size:-self.footer_size]  # Dane użytkownika

        footer = frame[-self.footer_size:]  # Stopka (sumy kontrolnej)

        return header, data, footer

    # wysyła ramkę ACK
    def send_ack(self, frame_number, is_end, FCS_type):
        # ramka:    dane,       numer ramki, czy ostatnia, typ sumy konrolnej
        header = b'\x00' + bytearray([frame_number, is_end, FCS_type])

        # suma kontrolna
        footer = FCS.encode(self.FCS_type, header)

        frame = header + footer
        return frame
