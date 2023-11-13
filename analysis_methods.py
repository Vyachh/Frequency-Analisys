import mpld3
from scipy.stats import spearmanr
import numpy as np
import matplotlib.pyplot as plt
import file_paths as fp

label_fontsize = 7
max_textsize = 40

def calculate_corr_method(x, y, method):
    if method == 'pearson':
        return np.corrcoef(x, y)[0, 1]
    elif method == 'spearman':
        return spearmanr(x, y)[0]
    else:
        raise ValueError("Неподдерживаемый метод корреляции")

def plot_correlation(freqs_list, filenames, method,title):
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    for j, ax in enumerate(axes.flatten()):
        common_words = set(freqs_list[0].keys()) & set(freqs_list[j+1].keys())
        
        x = np.array([freqs_list[0][word] for word in common_words], dtype=np.float64)
        y = np.array([freqs_list[j+1][word] for word in common_words], dtype=np.float64)
        
        corr_value = calculate_corr_method(x, y, method)
        # Названия осей
        xlabel = filenames[j].replace(fp.default_path_files, '')[:max_textsize]
        ylabel = filenames[0].replace(fp.default_path_files, '')[:max_textsize]
        
        ax.set_xlabel(f'Частоты в {xlabel}...',fontsize = label_fontsize)
        ax.set_ylabel(f'Частоты в {ylabel}...',fontsize = label_fontsize)
        
        ax.scatter(x, y)
        ax.set_title(f'Корреляция {title.capitalize()}: {corr_value:.2f}')

    mpld3.save_html(fig, fp.default_path_figures + f"{title}.html")
    plt.tight_layout()
    plt.show()

def pearson(freqs_list=[], filenames=[]):
    plot_correlation(freqs_list, filenames,"pearson", 'Корреляция Пирсона')

def spearman(freqs_list=[], filenames=[]):
    plot_correlation(freqs_list, filenames,"spearman", 'Корреляция Спирмена')

def odds_ratios(freqs_list = [], filenames = []):        
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))        
        for j, ax in enumerate(axes.flatten()):
            
            # Расчет корреляции Отношения шансов
            common_words = set(freqs_list[0].keys()) & set(freqs_list[j+1].keys())
            odds_ratios = {}            
            for word in common_words:
                a = np.array([freqs_list[0][word]], dtype=np.float64)
                b = np.array([sum(freqs_list[0].values()) - a], dtype=np.float64)
                c = np.array([freqs_list[j+1][word]], dtype=np.float64)
                d = np.array([sum(freqs_list[j+1].values()) - c], dtype=np.float64)
                odds_ratio = (a * d) / (b * c)
                odds_ratios[word] = odds_ratio
                
            # Получение точек
            words = list(odds_ratios.keys())
            values = list(odds_ratios.values())
            
            # Названия осей
            xlabel = filenames[j].replace(fp.default_path_files,'')[:max_textsize]
            ylabel = filenames[0].replace(fp.default_path_files,'')[:max_textsize]
            
            ax.set_xlabel(f'Частоты в {xlabel}...',fontsize = label_fontsize, color = 'blue', horizontalalignment = 'left', verticalalignment = 'bottom')
            ax.set_ylabel(f'Частоты в {ylabel}...',fontsize = label_fontsize)
            
            # Меняем местами x и y
            ax.scatter( values, words) 
            ax.set_title('Отношение шансов')     
            
        mpld3.save_html(fig, fp.default_path_figures + "odds_ratios.html")
        plt.tight_layout()
        plt.show()
