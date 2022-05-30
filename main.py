import os
from datetime import datetime
import re
import matplotlib.pyplot as plt
import logging
import numpy as np


def sort_and_analysis(directory):
    logger = logging.getLogger('logger')
    logging.basicConfig(level=logging.INFO)
    times = []
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
            logger.info('Opened file ' + str(filename))
            text = f.read()
            f.close()
            word_list = re.split("\W+", text)
            word_list = list(filter(lambda x: x != '', word_list))
            start = datetime.now()
            for i in range(len(word_list) - 1):  # Сложность О(n^2)
                logger.info('Sorted: ' + str(int(round(i/len(word_list), 2)*100)) + '%')
                for j in range(len(word_list) - i - 1):
                    if len(word_list[j]) < len(word_list[j + 1]):
                        word_list[j], word_list[j + 1] = word_list[j + 1], word_list[j]
            time_sort = datetime.now() - start
            times.append([len(word_list), time_sort.microseconds])
            count = {}
            for w in word_list:  # Сложность О(n)
                count[len(w)] = count.get(len(w), 0) + 1

            result = open(os.path.join('result/', filename), 'w')
            logger.info('Writing the result...')
            result_list = []
            for i in range(len(word_list)-1):
                result_list.append(word_list[i] + '\n')
            result.writelines(result_list)
            result.close()

            analysis = open(os.path.join('analysis/', filename), 'w')
            logger.info('Writing the analysis...')
            analysis_list = 'Введённый текст:\n'
            analysis_list += text + '\n'
            analysis_list += '\n'
            analysis_list += 'Вариант 7:\nЛатиница,по количеству символов в слове, по убыванию,' \
                             ' учитывать числа, сортировка Пузырьком\n'
            analysis_list += 'Количество слов: ' + str(len(word_list)) + '\n'
            analysis_list += 'Время сортировки: ' + str(time_sort) + '\n'
            analysis_list += 'Количество слов каждой длины:\n'
            for a, b in count.items():
                analysis_list += str(a) + ': ' + str(b) + '\n'
            analysis.writelines(analysis_list)
            analysis.close()
            logger.info('Done: ' + filename)

    times = sorted(times, key=lambda time: time[1])

    times = np.asarray(times)
    plt.figure(figsize=(12, 8))
    plt.plot(times[:, 1], times[:, 0])
    plt.xlabel('Время выполнения (мкс)')
    plt.ylabel('Количество слов')
    plt.show()

if __name__ == '__main__':
    sort_and_analysis('books')
