import threading
import time

# Create a semaphore with a value of 3
semaphore = threading.Semaphore(3)

def display(name):
    for i in range(5):
        print(f"{name} is accessing the resource.")
        semaphore.acquire()
        print(f"{name} has acquired the resource.")
        time.sleep(1)
        print(f"{name} is releasing the resource.")
        semaphore.release()
        print()

# Create 5 threads
threads = []
for i in range(5):
    t = threading.Thread(target=display, args=(f"Thread {i}",))
    threads.append(t)
    t.start()

# Wait for all threads to finish
for t in threads:
    t.join()