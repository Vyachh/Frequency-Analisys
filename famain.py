import asyncio
import falib as fl

async def main():
    fl.clear_console()
    print("\tЗадание по сдаче курса «Информационные технологии», “Информационные системы”. Анализ данных:\n")
    await fl.init()

asyncio.run(main())
print("Done...") 

