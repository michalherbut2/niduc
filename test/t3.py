import asyncio

class Transmitter:
    def __init__(self):
        self.queue = asyncio.Queue()

    async def delayed_task(self, d):
        await asyncio.sleep(2)
        print("dodano", d)
        # Po zakończeniu zadania, dodajemy do kolejki informację o zakończeniu
        await self.queue.put(None)

    async def main(self):
        print("Program zaczął działać.")

        # Tworzymy zadania i dodajemy je do kolejki
        tasks = [self.delayed_task(i) for i in range(1, 21)]
        for task in tasks:
            await self.queue.put(task)

        # Wyjmujemy zadania z kolejki i uruchamiamy je
        while True:
            task = await self.queue.get()
            if task is None:
                break
            await asyncio.create_task(task)

        print("Program zakończył działanie.")

transmitter = Transmitter()
asyncio.run(transmitter.main())
