import asyncio
import falib as fl
import file_paths as fp

async def main():
    fl.clear_console()
    
    file_info = fp.scan_folder()
    file_names = file_info[0]
    file_paths = file_info[1]
    tasks = [fl.read_file(file_path) for file_path in file_paths]
    text = await asyncio.gather(*tasks)

    freqs_list = []
    results_lines = []
    freq_list_normalized = []
    freq_list_normalized_sorted = []

    print("\tЗадание по сдаче курса «Информационные технологии», “Информационные системы”. Анализ данных:\n")
    await fl.start_freq_analyze(file_names, text, freqs_list, results_lines, freq_list_normalized,freq_list_normalized_sorted)
    await fl.switch(file_names, results_lines, freqs_list, freq_list_normalized, freq_list_normalized_sorted)

asyncio.run(main())
print("Done...")

# Возможные улучшения
# написать кнопку "назад" c очисткой консоли
# добавить новый freq_list_normalized_sorted, с отсеиванием слов, встречающихся 1-2 раза
# 
# 
# 
# 
