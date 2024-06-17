import asyncio

class Transmitter:


    async def delayed_task(self):
        await asyncio.sleep(5)
        print("Coś ma się zmienić po 5 sekundach")

    async def main(self):
        print("Program zaczął działać.")
        
        # Uruchomienie funkcji delayed_task() z limitem czasu 2 sekund
        try:
            await asyncio.wait_for(self.delayed_task(), timeout=2)
        except asyncio.TimeoutError:
            print("Przekroczono limit czasu (2 sekundy) dla zadania.")

        print("Program zakończył działanie.")
        a=1024
        length = (a.bit_length() + 7) // 8
        print(a.to_bytes(length))
        print(0x0.to_bytes())

siema= Transmitter()

asyncio.run(siema.main())
