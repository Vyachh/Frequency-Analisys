import os

def scan_folder(folder_path, extension):
    file_dict = {}
    script_path = os.path.dirname(os.path.abspath(__file__))
    folder_abs_path = os.path.join(script_path, folder_path)
    
    for root, dirs, files in os.walk(folder_abs_path):
        for file in files:
            if file.endswith('.' + extension):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, script_path)
                file_dict[file] = rel_path
    
    return file_dict

folder_path = 'docs\\'
extension = 'txt'
files = scan_folder(folder_path, extension)
print(files)


import pymorphy2

# Пример массива freqs_list
freqs_list = [('красавица', 1),('красивый', 2),( 'красота', 3),( 'красивенький', 4),( 'покрасоваться',5),( 'перекрасить',6),( 'по-любому',4),('бурить', 7),( 'бурильщик',5),( 'буровая',6),( 'бур',7),('буря', 8),( 'бурный',9),( 'буревестник',5)]

morph = pymorphy2.MorphAnalyzer()

processed_freqs = {}

for word, freq in freqs_list:
    # Лемматизируем русское слово
    lemma = morph.parse(word)[0].normal_form
    
    if lemma in processed_freqs:
        processed_freqs[lemma] += freq
    else:
        processed_freqs[lemma] = freq

processed_freqs_list = list(processed_freqs.items())

print(processed_freqs_list)