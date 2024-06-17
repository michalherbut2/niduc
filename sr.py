import time

class SelectiveRepeatARQ:
    def __init__(self, sender, receiver, window_size):
        self.sender = sender
        self.receiver = receiver
        self.window_size = window_size

    def send_data(self, data):
        start_seq = 0
        end_seq = min(self.window_size, len(data))
        while start_seq < len(data):
            window = data[start_seq:end_seq]
            self.sender.send(window)

            start_time = time.time()
            acks_received = self.receiver.receive_ack(start_seq, end_seq)
            end_time = time.time()

            for seq in range(start_seq, end_seq):
                if seq in acks_received:
                    print(f"ACK {seq} received. Transmission successful!")
                else:
                    print(f"Timeout occurred for ACK {seq}. Retransmitting...")

            start_seq = end_seq
            end_seq = min(start_seq + self.window_size, len(data))

    def receive_data(self, data):
        self.receiver.receive(data)

class Sender:
    def __init__(self):
        pass

    def send(self, data):
        print("Sending data:", data)

class Receiver:
    def __init__(self):
        pass

    def receive(self, data):
        print("Receiving data:", data)

    def receive_ack(self, start_seq, end_seq):
        acks = input("Enter ACKs received (e.g., 0 1 2): ")
        return [int(seq) for seq in acks.split()]

# Przykładowe użycie
sender = Sender()
receiver = Receiver()

arq = SelectiveRepeatARQ(sender, receiver, window_size=3)
arq.send_data("Hello World")
