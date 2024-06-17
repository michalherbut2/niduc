import asyncio

class Transmitter:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.semaphore = asyncio.Semaphore()  # Ustawiamy maksymalną liczbę jednocześnie wykonywanych zadań na 2

    async def delayed_task(self, d):
        print("start", d)
        await asyncio.sleep(4)  # Zadanie trwa 4 sekundy
        print("end", d)
        self.semaphore.release()  # Zwolnienie semafora po zakończeniu zadania

    async def add_tasks_to_queue(self):
        for i in range(1, 21):
            await asyncio.sleep(1)  # Dodaj nowe zadanie co sekundę
            await self.semaphore.acquire()  # Czekaj na dostęp do semafora
            await self.queue.put(self.delayed_task(i))

    async def execute_tasks(self):
        while True:
            task = await self.queue.get()
            await asyncio.create_task(task)

 
    async def calctime(self):
         # Wykonywanie innych operacji w czasie oczekiwania
        for i in range(60):
            print("czas:", i)
            await asyncio.sleep(1)  # Oczekiwanie przez 1 sekundę

    async def main(self):
        print("Program zaczął działać.")

        asyncio.create_task(self.calctime())

        # Uruchamiamy dwie funkcje równolegle
        await asyncio.gather(
            self.add_tasks_to_queue(),
            self.execute_tasks()
        )

       
        print("Program zakończył działanie.")

transmitter = Transmitter()
asyncio.run(transmitter.main())
