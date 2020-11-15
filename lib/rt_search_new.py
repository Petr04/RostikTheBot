from googlesearch import search
import numpy as np
from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance_ndarray
import pymorphy2

keywords = (
    (('internet', 'mobile'), (
        'интернет', 'инет', 'web', 'браузер'
    )),
    (('internet'), (
        'браузер', 'роутер',
    )),
    (('mobile'), (
        'сим',
    )),
    (('phone'), (
        'домашний', 'стационарный',
    )),
    (('video'), (
        'камера', 'видеокамера', 'дом', 'умный', 'наблюдение', 'видеонаблюдение',
    )),
)

dictionary = []
for _, words in keywords:
    dictionary += words

def fix_word(text, words=dictionary):
    array = np.array(words)

    result = list(zip(words, list(normalized_damerau_levenshtein_distance_ndarray(text, array))))

    command, rate = min(result, key=lambda x: x[1])

    # Подобранное значение для определения совпадения текста среди значений указанного списка
    # Если True, считаем что слишком много ошибок в слове, т.е. text среди all_commands нет
    if rate > 0.40:
        return

    return command

morph = pymorphy2.MorphAnalyzer()
def normal_form(word):
    return morph.parse(word)[0].normal_form

def possible_section(question):
    words = question.split()
    for i, word in enumerate(words):
        fixed = fix_word(word.lower())
        if (fixed == None):
            continue

        words[i] = normal_form(fixed)

    ret = []
    for sections, section_keywords in keywords:
        if len(set(words).intersection(set(section_keywords))) > 0:
            return sections

    return []

def rt_search(question, section, pages=3):
    if section == 'video':
        question+=' site:help.smarthome.rt.ru/'
    else:
        question+=' site:rt.ru/support/'+section
    # Google Search query results as a Python List of URLs
    return list(search(question, stop=pages, pause=1))

if __name__ == '__main__':
    while True:
        s = input()
        print(possible_section(s))

    # mylist=rt_search('умный дом', 'video')
    # print('\n'.join(mylist))
