from datetime import datetime
import os

from upper_logic import *

'''
Функция по выделению жирным шрифтом
'''

def bold_text(text):
    bold_start = '\033[1m'
    bold_end = '\033[0m'
    return bold_start + text + bold_end


'''
Функция по обозначению даты заметки
'''

def note_date():
    time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    return time


'''
Функция для создания директории приложения по следующему пути:C:\\Users\\user_name\\Documents
'''

def create_directory():
    user_name = os.environ.get("USERNAME")
    path = 'C:\\Users\\' + user_name + '\\Documents'
    if not os.path.isdir('C:\\Users\\' + user_name + '\\Documents\\aNotes'):
        os.mkdir('C:\\Users\\' + user_name + '\\Documents\\aNotes')


'''
Функция создания нового пользователя (ЕСТЬ БАГ ЕСЛИ ДОБАВИТЬ СУЩЕСТВУЮЩЕГО И ЗАТЕМ НОВОГО ТО ДАЕТ ОШИБКУ)
'''

def create_new_user():
    user_name = os.environ.get("USERNAME")
    user = input('Введите имя пользователя, непревышающее 12 символов >> ')
    if os.path.isdir('C:\\Users\\' + user_name + '\\Documents\\aNotes\\' + user):
        print('Данный пользователь уже существует. Введите другое имя.')
        create_new_user()
    if len(user) <= 12:
        os.mkdir('C:\\Users\\' + user_name + '\\Documents\\aNotes\\' + user)
    else:
        print('Введено неверное количество символов')
        create_new_user()


'''
Функция удаления пользователя
'''

def user_del():
    user_name = os.environ.get("USERNAME")
    path = 'C:\\Users\\' + user_name + '\\Documents\\aNotes'
    user_list = os.listdir(path)
    if len(user_list) == 0:
        print('В приложении никто не зарегистрирован\n'
              'Удаление невозможно')
    else:
        user_for_del = input('Введите имя пользвателя, которого необходимо удалить >> ')
        if not os.path.isdir('C:\\Users\\' + user_name + '\\Documents\\aNotes\\' + user_for_del):
            print('Данного пользователя не существует. Введите другое имя.')
            user_del()
        else:
            confirmation = input('Для подвтерждения удаления введите - yes\n'
                           'Для отмены введите - no\n'
                           'Для отмены действия введите - break\n'
                           'Ваша команда >> ')
            if confirmation =='yes':
                os.rmdir('C:\\Users\\' + user_name + '\\Documents\\aNotes\\' + user_for_del)
                print('Пользователь удален\n')
                help_info()
            elif confirmation == 'no':
                user_del()
                help_info()
            elif confirmation == 'break':
                user_select_info()


'''
Функция редактирования пользователя
'''

def user_edit():
    user_name = os.environ.get("USERNAME")
    path = 'C:\\Users\\' + user_name + '\\Documents\\aNotes'
    user_list = os.listdir(path)
    if len(user_list) == 0:
        print('В приложении никто не зарегистрирован\n'
              'Редактирование невозможно')
    else:
        user_for_edit = input('Введите имя пользователя для редактирования >> ')
        if not os.path.isdir('C:\\Users\\' + user_name + '\\Documents\\aNotes\\' + user_for_edit):
            print('Данного пользователя не существует. Введите другое имя.')
            user_edit()
            help_info()
        else:
            new_user = input('Введите имя пользователя, непревышающее 12 символов >> ')
            if len(new_user) <= 12:
                old_folder = 'C:\\Users\\' + user_name + '\\Documents\\aNotes\\' + user_for_edit
                new_folder = 'C:\\Users\\' + user_name + '\\Documents\\aNotes\\' + new_user
                os.rename(old_folder, new_folder)
                print('Редактирование завершено успешно\n')
            else:
                print('Введено неверное количество символов')
                user_edit()
                help_info()


'''
Функция вывода информация для последующего выбора команды пользователем
'''

def user_select_info():
    print('Выберите команду:\n'
          'list   - Вывести список пользователей\n'
          'choose - Выбрать пользователя\n'
          'add    - Добавить пользователя\n'
          'edit   - Редактировать пользователя\n'
          'del    - Удалить пользователя\n'
          'exit   - Завершить работу\n')


'''
Функция обработки команд пользователя
'''

def input_user_select(var):
    user_name = os.environ.get("USERNAME")
    path = 'C:\\Users\\' + user_name + '\\Documents\\aNotes'
    user_list = os.listdir(path)
    if var == 'exit':
        return var

    elif var == 'list':
        if len(user_list) == 0:
            print('В приложении еще никто не зарегистрирован\n'
                  'Присоединяйтесь!')
            create_new_user()
            help_info()

        elif len(user_list) > 0:
            for user in user_list:
                print(user)
            help_info()

    elif var == 'add':
        create_new_user()
        help_info()

    elif var == 'help':
        user_select_info()

    elif var == 'del':
        user_del()

    elif var == 'edit':
        user_edit()
    

'''
Функция вызова информации для помощи пользователю
'''

def help_info():
    print('\nВведите help для вывода списка команд\n')

