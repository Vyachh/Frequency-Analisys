import os

def scan_folder():
    # Инициализация пустых списков для хранения имен файлов и их относительных путей
    file_names = []
    file_paths = []
    folder_path = 'docs\\'
    extension = 'txt'
    # Получение абсолютного пути к текущему скрипту
    script_path = os.path.dirname(os.path.abspath(__file__))
    
    # Соединение пути к папке скрипта и указанной папке для сканирования
    folder_abs_path = os.path.join(script_path, folder_path)
    
    # Обход всех файлов и подпапок в указанной папке
    for root, dirs, files in os.walk(folder_abs_path):
        for file in files:
            # Проверка, что файл имеет указанное расширение
            if file.endswith('.' + extension):
                # Формирование полного пути к файлу
                file_path = os.path.join(root, file)
                
                # Вычисление относительного пути от скрипта к файлу
                rel_path = os.path.relpath(file_path, script_path)
                
                # Добавление записей в соответствующие списки
                file_names.append(file)
                file_paths.append(rel_path)
    
    # Возврат двух списков с результатами сканирования
    return file_names, file_paths

default_path_files = r"docs\\"
default_path_results = r"results\\"
default_path_figures = r"results\figures\\"

# file_1_read = default_path_files + "1. Роман И.Ильфа, Е.Петрова ”Двенадцать стульев”, главы 1 и 2 .txt"
# file_2_read = default_path_files + "2. Рассказ И.Ильфа “Москва от зари до зари” Рассказ И.Ильфа “Случай в конторе”.txt"
# file_3_read = default_path_files + "3. Рассказ Е. Петрова “Рассказ об одном солнце” Рассказ Е. Петрова “Семейное счастье” .txt"
# file_4_read = default_path_files + "4. Рассказ М. Булгакова “Я убил” Повесть М. Булгакова “Собачье сердце”, главы 1 и 2.txt"
file_result_write = default_path_results + "result.txt"