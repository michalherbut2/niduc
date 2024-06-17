
import asyncio

class Transmitter:
    async def delayed_task(self,d):
        await asyncio.sleep(2)
        print("dodano 1")

    async def main(self):
        print("Program zaczął działać.")
        asyncio.create_task(self.delayed_task(1))
        await asyncio.sleep(3)  # Oczekiwanie przez 1 sekundę
        print("Program zakończył działanie.")

    
transmitter = Transmitter()

asyncio.run(transmitter.main())