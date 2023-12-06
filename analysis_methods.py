import time
import mpld3
import numpy as np
import matplotlib.pyplot as plt
import file_paths as fp
from matplotlib import cm
from scipy.stats import spearmanr
from collections import Counter

label_fontsize = 7
max_textsize = 40

# def optimize_freqs_lists(list1, list2):
#     joint_list = list1 + list2

#     optimized_list1 = separate(joint_list.copy(), list1)
#     optimized_list2 = separate(joint_list.copy(), list2)

#     return optimized_list1, optimized_list2

# def separate(main_text, separated_text):
#     for word2 in separated_text:
#         for word1 in main_text: 
#             if(word1 == word2):
#                  main_text[word1] = 0
#     return main_text

def pad_arrays(array1, array2):
    max_length = max(len(array1), len(array2))
    for i in range(max_length):
        counter1 = array1 if i < len(array1) else Counter()
        counter2 = array2 if i < len(array2) else Counter()
        all_words = set(counter1.keys()).union(set(counter2.keys()))
        for word in all_words:
            if word not in counter1:
                counter1[word] = 0
            if word not in counter2:
                counter2[word] = 0
        array1[i] = counter1
        array2[i] = counter2
    return array1, array2

def calculate_corr_method(x, y, method):
    if method == 'pearson':
        return np.corrcoef(x, y)[0, 1]
    elif method == 'spearman':
        return spearmanr(x, y)[0]
    else:
        raise ValueError("Неподдерживаемый метод корреляции")

def plot_correlation(freqs_list, filenames, title):
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    for j, ax in enumerate(axes.flatten()):

        first_list, second_list = pad_arrays(freqs_list[0].copy(), freqs_list[j + 1].copy())
        common_words = set(freqs_list[0].keys()) & set(freqs_list[j + 1].keys())

        x = np.array([first_list[word] for word in common_words], dtype=np.float64)
        y = np.array([second_list[word] for word in common_words], dtype=np.float64)


        corr_value = np.corrcoef(x, y)[0, 1]
        # Названия осей
        xlabel = filenames[j + 1].replace(fp.default_path_files, '')[:max_textsize]
        ylabel = filenames[0].replace(fp.default_path_files, '')[:max_textsize]

        ax.set_xlabel(f'Частоты в {xlabel}...', fontsize=label_fontsize)
        ax.set_ylabel(f'Частоты в {ylabel}...', fontsize=label_fontsize)

        colors = cm.viridis(x / np.max(y))
        ax.scatter(x, y, c=colors)
        ax.set_title(f'Корреляция {title.capitalize()}: {corr_value:.2f}')

    mpld3.save_html(fig, fp.default_path_figures + f"{title}.html")
    plt.tight_layout()
    plt.show()

def pearson(freqs_list=[], filenames=[]):
     plot_correlation(freqs_list, filenames, 'Корреляция Пирсона')

def spearman(freqs_list=[], filenames=[]):
    plot_correlation(freqs_list, filenames, 'Корреляция Спирмена')
    
def odds_ratios(freqs_list=[], filenames=[]):
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    for j, ax in enumerate(axes.flatten()):
        # Расчет корреляции Отношения шансов
        common_words = set(freqs_list[0].keys()) & set(freqs_list[j + 1].keys())

        a = np.array([freqs_list[0][word] for word in common_words], dtype=np.float64)
        b = np.array([sum(freqs_list[0].values()) - a], dtype=np.float64)
        c = np.array([freqs_list[j + 1][word] for word in common_words], dtype=np.float64)
        d = np.array([sum(freqs_list[j + 1].values()) - c], dtype=np.float64)

        odds_ratios = (a * d) / (b * c)

        # Получение точек
        words = list(common_words)
        values = list(odds_ratios)

        # Названия осей
        xlabel = filenames[j + 1].replace(fp.default_path_files, '')[:max_textsize]
        ylabel = filenames[0].replace(fp.default_path_files, '')[:max_textsize]

        ax.set_xlabel(f'Частоты в {xlabel}...', fontsize=label_fontsize, color='blue', verticalalignment='top')
        ax.set_ylabel(f'Частоты в {ylabel}...', fontsize=label_fontsize, color='blue')

        ax.scatter(values, words)
        ax.set_title('Отношение шансов')

    mpld3.save_html(fig, fp.default_path_figures + "odds_ratios.html")
    plt.tight_layout()
    plt.show()
