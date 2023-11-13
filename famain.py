import asyncio
import falib as fl
import file_paths as fp

async def main():
    fl.clear_console()

    # Пример текста для анализа
    filenames = [fp.file_1_read, fp.file_2_read, fp.file_3_read, fp.file_4_read]
    tasks = [fl.read_file(filename) for filename in filenames]
    text = await asyncio.gather(*tasks)
    
    freqs_list = []
    results_lines = []
    
    print("\tЗадание по сдаче курса «Информационные технологии», “Информационные системы”. Анализ данных:\n")
    fl.start_freq_analyze(filenames, text, freqs_list, results_lines)
    await fl.switch(filenames, results_lines, freqs_list)

asyncio.run(main())
print("Done...")