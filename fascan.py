import os

def scan_folder(folder_path, extension):
    # Инициализация пустых списков для хранения имен файлов и их относительных путей
    file_names = []
    file_paths = []
    
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

folder_path = 'docs\\'
extension = 'txt'


import pymorphy2

# Пример массива freqs_list
freqs_list = [('красавица', 1), ('красивый', 2), ('красота', 3), ('красивенький', 4), ('покрасоваться', 5),
              ('перекрасить', 6), ('по-любому', 4), ('бурить', 7), ('бурильщик', 5), ('буровой', 6),
              ('бур', 7), ('буря', 8), ('бурный', 9), ('буревестник', 5)]

def process_freqs_list(freqs_list):
    morph = pymorphy2.MorphAnalyzer()

    processed_freqs = {}

    for word, freq in freqs_list:
    # Получаем нормальную форму слова
        lemma = morph.parse(word)[0].normal_form
    
    # Получаем корень слова
        root = morph.parse(lemma)[0].lexeme[0].word
    
    # Если корень уже есть в словаре, увеличиваем его частоту
        if root in processed_freqs:
            processed_freqs[root] += freq
        else:
        # Если корень отсутствует, добавляем его в словарь
            processed_freqs[root] = freq

# Преобразуем словарь в список кортежей
    processed_freqs_list = list(processed_freqs.items())
    return processed_freqs_list







