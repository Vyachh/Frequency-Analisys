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

# async
def stem_lemma(freqs_list):
    morph = pymorphy2.MorphAnalyzer()
    stemmer = SnowballStemmer("russian")
    stem_lemma_list = Counter()
    # Проходимся по каждому слову в freqs_list
    for word, freq in freqs_list[0].items():
    
        # Получаем нормльную форму слова с помощью pymorphy2
        lemma = morph.parse(word)[0].normal_form
        # Получаем стем (неизменяемую форму) слова с помощью nltk.stem
        stem_word = stemmer.stem(lemma)
    
        stem_lemma_list[stem_word] += freq

    return [stem_lemma_list]

async def read_file(path):
    async with aiofiles.open(path, "r", encoding="utf-8") as file:
        text = await file.read()
        return text

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

#Анализ длины предложений
def sents_analyze(text):
    sentences = nltk.sent_tokenize(text) 
    word_counts = []
    for sentence in sentences:
        words = nltk.word_tokenize(sentence)
        word_counts.append(len(words))

    return word_counts, len(sentences)


def clear_console():
    os.system("cls")


def start_freq_analyze(filenames, text, freqs_list, results_lines, freqs_list_normalized):
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

        # Сортировка частотного анализа по убыванию частоты
        sorted_freqs = dict(sorted(freqs.items(), key=lambda x: (-x[1], x[0])))
        
        text_append(filenames, results_lines, r, average, sorted_freqs)
    
    # # freqs_list_normalized = freqs_list
    freqs_list_normalized = stem_lemma(freqs_list)
    return freqs_list_normalized

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

async def switch(filenames, results_lines, freqs_list, freqs_list_normalized):
    while True:
        # Выбор пользователя на вывод данных
        choice = input("Вывести все результаты в файл (Y)?\n"+
                       "Вывести все результаты в файл в консоль (N)?\n"+
                       "Вывести определенный текст(T)?\n"+
                       "Загрузить корреляции с уникальностью (X)?:\n"+
                       "Загрузить корреляции с нормализацией (Z)?:")
                       
        clear_console()

        if choice.lower().startswith("y"):
            # Вывод результатов в файл
            async with aiofiles.open(fp.file_result_write, 'w', encoding="utf-8") as result_file:
                # Перебираем вложенные массивы и записываем данные в файл
                for text_data in results_lines:
                    await result_file.writelines(text_data)
            break

            # Вывод результатов в консоли
            # Перебираем вложенные массивы и выводим данные в консоли
        elif choice.lower().startswith("n"):
            for text_data in results_lines:
                print("\n".join(text_data))
            break

            # Вывод результата определенного текста в консоль
        elif choice.lower().startswith("t"):
            number = 1
            for filename in filenames:
                print(f"{number}: {filename}")
                number = number + 1
                
            await print_selected_text(results_lines, choice)
            break

        #Загрузка новой корреляции
        elif choice.lower().startswith("z"):
            print(freqs_list_normalized)
            am.pearson(freqs_list_normalized, filenames)
            am.spearman(freqs_list_normalized, filenames)
            am.odds_ratios(freqs_list_normalized, filenames)
            break

        #Загрузка корреляции
        elif choice.lower().startswith("x"):
            am.pearson(freqs_list, filenames)
            am.spearman(freqs_list, filenames)
            am.odds_ratios(freqs_list, filenames)
            print("Корреляции сохранены.")
            break
            
        else:
            print("Некорректный выбор. Введите 'Y'/'N'/'T'/'X'/'Z'.")

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



#{#Анализ одного предложения
# def sent_tokenize(text):
#     sentences = []
#     sentence = ""
#     for char in text:
#         sentence += char
#         if check_mark(char):
#             sentences.append(sentence)
#             sentence = ""
#     return sentences

# #Поиск по знакам препинания
# def check_mark(char):
#     if char in ['?', '!', '.']:
#         return True
#     return False

#Анализ слов впредложении
# def word_tokenize(sentence):
#     chars = ""
#     words = []
#     for char in sentence:
#         chars += char
#         if char == " " or check_mark(char):
#             words.append(chars.strip())
#             chars = ""
#     return words}