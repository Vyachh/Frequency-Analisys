import asyncio
import file_paths as fp
import string
import aiofiles
import os
import analysis_methods as am
import pymorphy2
import nltk
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

file_names = []
file_paths = []

freqs_list = []
results_lines = []
freq_list_normalized = []
freq_list_normalized_sorted = []


#First step
async def start_freq_analyze(filenames, text, freqs_list, results_lines, freq_list_normalized, freq_list_normalized_sorted):
    for r, result in enumerate(text):
        # Анализ количества слов в предложениях
        sents_info = sents_analyze(result)
        # Вычисляем количество слов в предложениях
        word_count = sum(sents_info[0])
        # Вычисляем среднее значение слов в каждом предложении
        average = round(word_count / sents_info[1], 2)
        # Вызываем функцию частотного анализа и выводим результат
        freqs = freq_analyze(result)
        freqs_list.append(freqs)
        # Вызываем функцию stem_lemma и добавляем результат в freq_list_normalized
        stem_lemma_list = stem_lemma([freqs])
        freq_list_normalized.append(stem_lemma_list)
        
        # Сортировка частотного анализа по убыванию частоты
        sorted_freqs = dict(sorted(freqs.items(), key=lambda x: (-x[1], x[0])))
        
        text_append(filenames, results_lines, r, average, sorted_freqs)
        #for end
    cutout_freqs(freq_list_normalized, freq_list_normalized_sorted,cut_threshold=2)

def cutout_freqs(freq_list_normalized, freq_list_normalized_sorted, cut_threshold):
    for freqs in freq_list_normalized:
        sorted_freqs = {k: v for k, v in sorted(freqs.items(), key=lambda item: item[1], reverse=True)}
        sorted_freqs_filtered = {k: v for k, v in sorted_freqs.items() if v >= cut_threshold}
        freq_list_normalized_sorted.append(sorted_freqs_filtered)

#Анализ длины предложений
def sents_analyze(text):
    sentences = nltk.sent_tokenize(text) 
    word_counts = []
    for sentence in sentences:
        words = nltk.word_tokenize(sentence)
        word_counts.append(len(words))
    return word_counts, len(sentences)

def freq_analyze(text):
    # Загрузка стоп-слов, если необходимо
    #nltk.download('stopwords')##########################################_Первоначальная загрузка_
    string.punctuation += "…’„»«1234567890–-—№"
    filter = string.punctuation
    stop_wordsRU = set(stopwords.words('russian')) 
    stop_wordsEN = set(stopwords.words('english'))
    words = [word for word in text.translate(str.maketrans("", "", filter)).lower().split()]
    words = [word for word in words if word not in stop_wordsRU]
    words = [word for word in words if word not in stop_wordsEN]
    words = [word for word in words if words.count(word) >= 0]
    return Counter(words)

def stem_lemma(freqs_list):
    morph = pymorphy2.MorphAnalyzer()
    stemmer = SnowballStemmer("russian")
    stem_lemma_list = Counter()
    
    # Проходимся по каждому слову в freqs_list
    for freqs in freqs_list:
        for word, freq in freqs.items():
            # Получаем нормальную форму слова с помощью pymorphy2
            lemma = morph.parse(word)[0].normal_form
            # Получаем стем (неизменяемую форму) слова с помощью nltk.stem
            stem_word = stemmer.stem(lemma)
            
            stem_lemma_list[stem_word] += freq
    
    return stem_lemma_list

def text_append(filenames, results_lines, r, average, sorted_freqs):
    # Создаем подмассив для каждого текста
    text_data = []
        
    # Определение текста, перенос на строку и табуляция
    text_data.append(f'\n\nАнализ {filenames[r]}:\n')
        
    # Выводим среднее количество слов в предложениях
    text_data.append(f'Среднее значение слов в каждом предложении:{average}\n')
        
    # Выводим частоты слов в тексте
    text_data.append("Частоты слов в тексте:")
        
    # Выводим частотные слова
    print_freqs(results_lines, sorted_freqs, text_data)

def print_freqs(results_lines, sorted_freqs, text_data):
    i = 0
    x = 0
    for word, freqs in sorted_freqs.items():
        if freqs != x:
            x = freqs
            if x == freqs:
                i = 0
                text_data.append("\n")
            text_data.append(f"\n{freqs}:\n\t{word}, ")
        else:
            if i == 9:
                text_data.append("\n\t")
                i = 0
            if freqs > 1:
                text_data.append(f"{word}, ")
                i = i + 1
    # Добавляем вложенный массив в result_lines
    results_lines.append(text_data)


#Second step

async def init():
    file_info = fp.scan_folder()
    file_names = file_info[0]
    file_paths = file_info[1]
    tasks = [read_file(file_path) for file_path in file_paths]
    text = await asyncio.gather(*tasks)

    await start_freq_analyze(file_names, text, freqs_list, results_lines, freq_list_normalized,freq_list_normalized_sorted)
    while True:
        # Выбор пользователя на вывод данных
        choice = input("Вывести результаты частотной характеристики в файл (Y)?\n"+
                                "Вывести результаты частотной характеристики в консоль (N)?\n"+
                                "Вывести результаты определенного текста(T)?\n"+
                                "Загрузить уникальные корреляции (X)?\n"+
                                "Загрузить нормализованные корреляции (Z)?:\n"+
                                "Загрузить отфильтрованные корреляции (C)?:\n")
        
        clear_console()

        if choice.lower().startswith("y"):
            # Вывод результатов в файл
            await print_in_file(results_lines)
            break

            # Вывод результатов в консоли
        elif choice.lower().startswith("n"):
            print_in_console(results_lines)
            break

            # Вывод результата определенного текста в консоль
        elif choice.lower().startswith("t"):
            number = 1
            for filename in file_names:
                print(f"{number}: {filename}")
                number = number + 1
                
            await print_selected_text(results_lines, choice)
            break
        
        #Загрузка новой корреляции
        elif choice.lower().startswith("z"):
            load_correlations_normalized(file_names, freq_list_normalized)
            break
        
        #Загрузка корреляции
        elif choice.lower().startswith("x"):
            load_correlations(file_names, freqs_list)
            break

         #Загрузка корреляции
        elif choice.lower().startswith("c"):
            load_correlations(file_names, freq_list_normalized_sorted)
            break
        
            
        else:
            print("Некорректный выбор. Введите 'Y'/'N'/'T'/'X'/'Z'.")

def load_correlations(filenames, freqs_list):
       am.pearson(freqs_list, filenames),
       am.spearman(freqs_list, filenames),
       am.odds_ratios(freqs_list, filenames)
       print("Корреляции сохранены.")

def load_correlations_normalized(filenames, freq_list_normalized):
    am.pearson(freq_list_normalized, filenames),
    am.spearman(freq_list_normalized, filenames),
    am.odds_ratios(freq_list_normalized, filenames)
    print("Корреляции сохранены.")

def print_in_console(results_lines):
    for text_data in results_lines:
        print("\n".join(text_data))

async def print_in_file(results_lines):
    async with aiofiles.open(fp.file_result_write, 'w', encoding="utf-8") as result_file:
                # Перебираем вложенные массивы и записываем данные в файл
        for text_data in results_lines:
            await result_file.writelines(text_data)


async def print_selected_text(results_lines,choice_txt):
    while True:
        # Запрашиваем у пользователя номер текста для вывода
        choice_txt = input(f"Введите номер текста для вывода (от 1 до {format(len(results_lines))}):")
        if not choice_txt.isdigit():
            print(f"Некорректный номер текста. Введите номер от 1 до {len(results_lines)}):")
        else:
            choice_txt = int(choice_txt)
            if not (1 <= choice_txt <= len(results_lines)):
                print(f"Некорректный номер текста. Введите номер от 1 до {len(results_lines)}):")
            else:
                text_data = results_lines[choice_txt - 1]

                while True:
                    choice = input(f"Вывести результат {choice_txt} в файл (Y) или в консоль (N)? ")

                    if choice.lower().startswith("y"):
                        # Вывод результата в файл
                        async with aiofiles.open(fp.file_result_write, 'w', encoding="utf-8") as result_file:
                            await result_file.writelines(text_data)
                        break

                    elif choice.lower().startswith("n"):
                        # Вывод результата в консоли
                        print("\n".join(text_data))
                        break
                    else:
                        print("Некорректный выбор. Введите 'Y' или 'N'.")

def clear_console():
    os.system("cls")

async def read_file(path):
    async with aiofiles.open(path, "r", encoding="utf-8") as file:
        text = await file.read()
        return text