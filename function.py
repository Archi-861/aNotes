from datetime import datetime
import os
from upper_logic import enter_point, user_select
import lower_logic


def main():
    enter_point()
    user_select()
    #добавить вызов основных функций



def create_note():
    #file = open('note.txt', 'w', encoding='utf8')
    title = input('Введите название заметки >> ')
    text = input('Введите  содержание заметки >> ')
    return title, text

'''
Функция по обозначению важности заметки
'''

def note_relevance():
    relevance = input('Укажите цифрой от 1 до 3 степень важности заметки\n'
                               ' 1 - высокая степень важности\n'
                               ' 2 - средняя степень важности\n'
                               ' 3 - низкая степень важности\n'
                               '>> ')

    if int(relevance) == 1:
        relevance = 'Высокая степень важности'
    elif int(relevance) == 2:
        relevance = 'Средняя степень важности'
    elif int(relevance) == 3:
        relevance = 'Низкая степень важности'
    else:
        print('Вы ввели неверную команду!')
        note_relevance()

    return relevance


