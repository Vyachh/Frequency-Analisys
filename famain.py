import asyncio
import falib as fl
import file_paths as fp
import fascan as fa

async def main():
    fl.clear_console()
    # filenames = [fp.file_1_read, fp.file_2_read, fp.file_3_read, fp.file_4_read]
    extension = 'txt'
    file_info = fa.scan_folder(fp.default_path_files, extension)
    file_names = file_info[0]
    file_paths = file_info[1]
    tasks = [fl.read_file(file_path) for file_path in file_paths]
    text = await asyncio.gather(*tasks)
    
    freqs_list = []
    results_lines = []    

    print("Задание по сдаче курса «Информационные технологии», “Информационные системы”. Анализ данных:\n")
    fl.start_freq_analyze(file_names, text, freqs_list, results_lines)
    await fl.switch(file_names, results_lines, freqs_list)

asyncio.run(main())
print("Done...")