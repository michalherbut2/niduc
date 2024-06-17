class Counter:
    def __init__(self):
        self.sent = 0
        self.total = 0
        self.ok = 0
        self.error = 0
        self.ack_error = 0
        self.out_of_order = 0
        self.not_detected = 0
        self.not_detected_ack = 0

    def inc(self, a):
        a+=1

    def inc_sent(self):
        self.sent += 1

    def inc_ok(self):
        self.ok += 1

    def inc_error(self):
        self.error += 1

    def inc_ack_error(self):
        self.ack_error += 1

    def inc_out_of_order(self):
        self.out_of_order += 1

    def inc_not_detected(self):
        self.not_detected += 1

    def inc_not_detected_ack(self):
        self.not_detected_ack += 1
    
    def print_results(self):
        self.total = self.ok + self.error + self.not_detected + self.ack_error + self.out_of_order + self.not_detected_ack

        print("\n\nRESULTS:")
        print(f"sent,{self.sent}")
        print(f"total,{self.total}")
        print(f"ok,{self.ok}")
        print(f"error,{self.error}")
        print(f"ack_error,{self.ack_error}")
        print(f"out_of_order,{self.out_of_order}")
        print(f"not_detected,{self.not_detected}")
        print(f"not_detected_ack,{self.not_detected_ack}")
        