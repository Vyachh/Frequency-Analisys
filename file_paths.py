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
file_result_write = default_path_results + "result.txt"