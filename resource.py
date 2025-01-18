import  os
from support import *
import shutil
from datetime import datetime
import csv

user_name = os.environ.get("USERNAME")   #Информация для приветственного сообщения пользователю с обращением к имени пользователя операционной системы
path = 'C:\\Users\\' + user_name + '\\Documents\\aNotes'   #путь для создания директории приложения
path_user = 'C:\\Users\\' + user_name + '\\Documents\\aNotes\\Users'   #путь для создания директории пользователей приложения



def enter_point():
    """
    Функция для приветствия пользователя. Берет данные пользователя с системных настроек.
    :return: None
    """
    print('Привет, ' + user_name + '! \n'
          'Добро пожаловать в приложение aNotes!\n')



def user_select():
    """
    Функция по созданию директории приложения в пути path, текстового файла users.txt для хранения данных пользователей и вывод команд по пользователям.
    Функция получает переменную var с выбранной пользователем командой и передает в функцию input_user_select.
    Выполняются следующие проверки:
    1) Наличие уже созданной директории;
    2) Наличие уже созданного текстового файла;
    3) Проверка на ввод exit.
    :return: None
    """
    if not os.path.isdir(path):
        os.mkdir(path)

    if not os.path.isdir(path_user):
        os.mkdir(path_user)

    if not os.path.isfile('users.txt'):
        file = open(path + '\\users.txt', 'a', encoding='utf-8')
        file.close()

    user_select_info()

    while True:
        var = input('Введите команду >> ')
        user_var = input_user_select(var)

        if user_var == 'exit':   #удаление буферного файла по проверке пароля пользователя
            os.remove(path + '\\$$users.txt')
            return False



def input_user_select(var):
    """
    Функция обработки варианта команды пользователя.
    Команда list выводит список пользователей приложения. В случае отсутствия пользователей запускает функцию по созданию пользователя add_new_user.
    Команда exit закрывает приложение.
    Команда add запускает функцию по созданию пользователя user_add.
    Команда help выводит информативную функцию по списку команд user_select_info.
    Команда del запускает функцию по удалению пользователя user_del.
    Команда edit запускает функцию по редактированию пользователя user_edit.
    Команда login запускает функцию по выбору (авторизации) пользователя приложения user_login.
    Выполняются следующие проверки:
    1) Проверка на ввод exit;
    2) Проверка на ввод несоответствующий командам выше.
    :param var:str
    :return: None
    """
    user_list = os.listdir(path_user)

    if var == 'exit':
        return var

    elif var == 'list':

        if len(user_list) == 0:
            user_list_text()
            user_add()
            help_info()

        elif len(user_list) > 0:

            for user in user_list:
                print(user)
            help_info()

    elif var == 'add':
        user_add()
        help_info()

    elif var == 'help':
        user_select_info()

    elif var == 'del':
        user_del()

    elif var == 'edit':
        user_edit()

    elif var == 'login':
        user_login()

    else:
        error_input_1()
        help_info()



def user_add():
    """
    Функция по созданию нового пользователя в приложении. Создается запись в текстовый файл users.txt и создается директория с именем пользователя.
    Имя пользователя не должно превышать 12 символов. Дополнительно запрашивается необходимость установки пароля на учетную запись пользователя. Пароль ограничен 10 символами.
    Выполняются следующие проверки:
    1) Проверка на количество символов на вводе имени пользователя
    2) Наличие на уже созданного пользователя с таким же именем;
    3) Проверка на пустой ввод, ввод break и DELETED;
    4) Проверка на количество символов на вводе пароля пользователя.
    :return: None
    """
    while True:
        user = input('Введите имя пользователя, не превышающее 12 символов\n'
                     'Или введите break для выхода в предыдущее меню >> ')

        if user == '':
            user_add_text_1()
            continue

        if os.path.isdir(path_user + '\\' + user):
            user_add_text_2()
            continue

        if user == 'break':
            break

        if user == 'DELETED':
            user_add_text_1()
            continue

        if len(user) <= 12:
            os.mkdir(path_user + '\\' + user)
            new_path = path_user + '\\' + user
            user_add_text_3()

            while True:
                user_password = input('Добавьте пароль к учетной записи\n'
                                      'Или введите no - для отказа\n'
                                      'Пароль не должен превышать 10 знаков! >> ')

                if user_password == '':
                    user_add_text_6()
                    continue

                elif user_password == 'break':
                    break

                elif user_password == 'no':   #создание пользователя без пароля
                    with open(path + '\\users.txt', 'a', encoding='utf-8') as file:
                        file.write('user_name:' + user + '間')
                        file.write('user_password:NONE間')
                        file.write('user_path:' + new_path + '間\n')
                        return False

                elif len(user_password) <= 10:   #создание пользователя с паролем
                    with open(path + '\\users.txt', 'a', encoding='utf-8') as file:
                        file.write('user_name:' + user + '間')
                        file.write('user_password:' + user_password + '間')
                        file.write('user_path:' + new_path + '間\n')
                        user_add_text_5()
                        return False

                else:
                    error_input_2()
                    continue

        else:
            error_input_2()



def user_del():
    """
    Функция для удаления пользователя из приложения, а именно замена имени пользователя в текстовом файле users.txt на имя DELETED
    и удаление директории пользователя с заметками.
    Выполняются следующие проверки:
    1) Наличие данного пользователя в приложении;
    2) Наличие пароля пользователя;
    3) Проверка на пустой ввод, на ввод break и DELETED.
    :return: None
    """
    user_list = os.listdir(path_user)

    while True:
        if len(user_list) == 0:
            user_del_text_1()
            help_info()
            return False

        user_for_del = input('Введите имя пользователя, которого необходимо удалить\n'
                             'Или введите break для выхода в предыдущее меню >> ')

        if user_for_del == 'break' or user_for_del == 'Break':
            return False

        if user_for_del == 'DELETED':
            user_del_text_4()
            return  False

        if user_for_del != 'break' or user_for_del != 'Break':
            with open(path + '\\users.txt', 'r', encoding='utf-8') as file:
                if not 'user_name:' + user_for_del in file.read():
                    user_del_text_2()
                    return False

        if user_for_del == '':
            user_del_text_4()
            continue

        else:
            while True:
                user_authorization = user_for_del
                user_password = check_password(user_authorization)   #проверка пароля пользователя для удаления данных

                if user_password == 'NONE':
                    check_password_text_2()
                    user_del_text_3()
                    while True:
                        confirmation = input('Ваша команда (введите no для выхода в предыдущее меню) >> ')

                        if confirmation == 'yes':
                            shutil.rmtree(path_user + '\\' + user_for_del)
                            with open(path + '\\users.txt', 'r', encoding='utf-8') as file:
                                users = file.read()
                                new_status = users.replace(user_for_del, 'DELETED')
                            with open(path + '\\users.txt', 'w', encoding='utf-8') as file:
                                file.write(new_status)
                            print('\nПользователь удален\n')
                            help_info()
                            return False
                        if confirmation == 'no':
                            help_info()
                            return False

                else:
                    input_password = input('\nВведите пароль для продолжения\n'
                                           'Или введите break для выхода в предыдущее меню >> ')

                    if input_password == 'break' or input_password == 'Break':
                        help_info()
                        return False

                    if input_password == user_password:
                        check_password_text_2()
                        user_del_text_3()
                        while True:
                            confirmation = input('Ваша команда (введите no для выхода в предыдущее меню) >> ')

                            if confirmation =='yes':
                                shutil.rmtree(path_user + '\\' + user_for_del)
                                with open(path + '\\users.txt', 'r', encoding='utf-8') as file:
                                    users = file.read()
                                    new_status = users.replace(user_for_del, 'DELETED')
                                with open(path + '\\users.txt', 'w', encoding='utf-8') as file:
                                    file.write(new_status)
                                print('\nПользователь удален\n')
                                help_info()
                                return False
                            if confirmation == 'no':
                                help_info()
                                return False

                    if input_password != user_password:
                        check_password_text_1()
                        help_info()
                        return False



def user_login():
    """
    Функция по выбору (авторизации) пользователя для последующей работы с интерфейсом заметок.
    Запускает функцию note_main.
    Выполняются следующие проверки:
    1) Наличие введенного пользователя в приложении;
    2) Проверка на пустой ввод, ввод break, DELETED;
    3) Проверка на соответствие пароля пользователя.
    :return: None
    """
    user_list = os.listdir(path_user)

    while True:
        if len(user_list) == 0:
            user_login_text_1()
            help_info()
            return False

        user_for_login = input('Введите имя пользователя\n'
                                'Или введите break для выхода в предыдущее меню >> ')

        if user_for_login == 'break' or user_for_login == 'Break':
            return False

        if user_for_login == 'DELETED':
            user_login_text_3()
            return False

        if user_for_login != 'break' or user_for_login != 'Break':
            with open(path + '\\users.txt', 'r', encoding='utf-8') as file:
                if not 'user_name:' + user_for_login in file.read():
                    user_login_text_2()
                    return False

        if user_for_login == '':
            user_login_text_3()
            continue

        else:
            while True:
                user_authorization = user_for_login
                user_password = check_password(user_authorization)

                if user_password == 'NONE':
                    check_password_text_2()
                    while True:
                        user = user_for_login
                        action = input('Введите команду для заметок>> ')
                        note_main(action, user)
                        note_help_info()
                        if action == 'exit' or action == 'Exit':
                            return False

                else:
                    input_password = input('\nВведите пароль для продолжения\n'
                                           'Или введите break для выхода в предыдущее меню >> ')

                    if input_password == 'break' or input_password == 'Break':
                        help_info()
                        return False

                    if input_password == user_password:
                        check_password_text_2()
                        note_menu()

                        while True:
                            user = user_for_login
                            action = input('Введите команду для заметок>> ')
                            note_main(action, user)
                            note_help_info()
                            if action == 'exit' or  action == 'Exit':
                                return False

                    if input_password != user_password:
                        check_password_text_1()
                        help_info()
                        return False



def user_edit():
    """
    Функция по редактированию имени пользователя приложения путем перезаписи файла users.txt и изменение директории пользователя.
    Выполняются следующие проверки:
    1) Наличие введенного пользователя в приложении;
    2) Проверка на пустой ввод, ввод break, DELETED;
    3) Проверка на соответствие пароля пользователя.
    :return: None
    """
    user_list = os.listdir(path_user)

    while True:
        if len(user_list) == 0:
            user_edit_text_1()
            help_info()
            return False

        user_for_edit = input('Введите имя пользователя для редактирования\n'
                              'Или введите break для выхода в предыдущее меню >> ')

        if user_for_edit == 'break' or user_for_edit == 'Break':
            return False

        if user_for_edit == 'DELETED':
            user_edit_text_3()
            return False

        if user_for_edit != 'break' or  user_for_edit != 'Break':
            with open(path + '\\users.txt', 'r', encoding='utf-8') as file:
                if not 'user_name:' + user_for_edit in file.read():
                    user_edit_text_2()
                    return False

        if user_for_edit == '':
            user_edit_text_3()
            continue

        else:
            while True:
                user_authorization = user_for_edit
                user_password = check_password(user_authorization)

                if user_password == 'NONE':
                    check_password_text_2()
                    while True:
                        new_user = input('Введите новое имя пользователя\n'
                                         'Или break для выхода в предыдущее меню >> ')

                        if new_user == 'break' or new_user == 'Break':
                            help_info()
                            return False

                        else:
                            if new_user == '':
                                user_edit_text_3()
                                continue

                            if os.path.isdir(path_user + '\\' + new_user):
                                user_edit_text_4()
                                continue

                            if new_user == 'DELETED':
                                user_edit_text_3()
                                continue

                            if len(new_user) <= 12:
                                shutil.copytree(path_user + '\\' + user_for_edit, path_user + '\\' + new_user)
                                shutil.rmtree(path_user + '\\' + user_for_edit)
                                with open(path + '\\users.txt', 'r', encoding='utf-8') as file:
                                    users = file.read()
                                    new_status = users.replace(user_for_edit, new_user)
                                with open(path + '\\users.txt', 'w', encoding='utf-8') as file:
                                    file.write(new_status)
                                    print('\nПользователь успешно изменен\n')
                                    help_info()
                                    break

                            else:
                                error_input_2()
                                return False

                else:
                    input_password = input('\nВведите пароль для продолжения\n'
                                           'Или введите break для выхода в предыдущее меню >> ')

                    if input_password == 'break' or input_password == 'Break':
                        help_info()
                        return False

                    if input_password == user_password:
                        check_password_text_2()
                        while True:
                            new_user = input('Введите новое имя пользователя\n'
                                             'Или break для выхода в предыдущее меню >> ')

                            if new_user == 'break' or new_user == 'Break':
                                help_info()
                                break

                            else:
                                if new_user == '':
                                    user_edit_text_3()
                                    continue

                                if os.path.isdir(path_user + '\\' + new_user):
                                    user_edit_text_4()
                                    continue

                                if new_user == 'DELETED':
                                    user_edit_text_3()
                                    continue

                                if len(new_user) <= 12:
                                    shutil.copytree(path_user + '\\' + user_for_edit, path_user + '\\' + new_user)
                                    shutil.rmtree(path_user + '\\' + user_for_edit)
                                    with open(path + '\\users.txt', 'r', encoding='utf-8') as file:
                                        users = file.read()
                                        new_status = users.replace(user_for_edit, new_user)
                                    with open(path + '\\users.txt', 'w', encoding='utf-8') as file:
                                        file.write(new_status)
                                        print('\nПользователь успешно изменен\n')
                                        help_info()
                                        break

                                else:
                                    error_input_2()

                    if input_password != user_password:
                        check_password_text_1()
                        help_info()
                        return False



def user_select_info():
    """
    Информативная функция для вывода списка команд по пользователям.
    :return: None
    """
    user_select_info_text()



def help_info():
    """
    Информативная функция для вывода текстовой информации по команде help.
    :return: None
    """
    help_info_text()


def note_main(action, user):
    """
    Функция по обработке команд по интерфейсу заметок, принимает параметр action (команда пользователя) и user(авторизованного пользователя).
    :param action: str
    :param user: str
    :return: None
    """

    if action == 'exit':
        return False

    elif action == 'create':
        note_add(user)

    elif action == 'list':
        note_list(user)

    elif action == 'del':
        del_note(user)

    elif action == 'help':
        note_menu()

    elif action == 'find':
        find_note(user)

    elif action == 'edit':
        edit_note(user)

    elif action == 'import':
        import_note(user)

def note_add(user):
    """
    Функция по созданию заметки пользователя. Заметка содержит название, содержание и важность, принимает параметр user(авторизованного пользователя).
    :param user: str
    :return: None
    """
    count_max = 1
    if not os.path.isfile(path_user + '\\' + user + '\\' + 'note_count.txt'):
        file = open(path_user + '\\' + user + '\\note_count.txt', 'w', encoding='utf-8')
        file.write('1')
        file.close()
    else:
        with open(path_user + '\\' + user + '\\' + 'note_count.txt', 'r', encoding='utf-8') as fl:
            counter = fl.read()
            if count_max <= int(counter):
                count_max = int(counter) + count_max
                with open(path_user + '\\' + user + '\\' + 'note_count.txt', 'w', encoding='utf-8') as fli:
                    fli.write(str(count_max))

    with open(path_user + '\\' + user + '\\' + 'note_' + user + '.txt', 'a', encoding='utf-8') as file:
        file.write('Заметка № ' + str(count_max) + '間')
        title_user = input('Введите название заметки >> ')
        text_user = input('Введите  содержание заметки >> ')
        file.write('Наименование = ' + title_user + '間')
        file.write('Содержание = ' + text_user + '間')
        while True:
            relevance = input('Укажите цифрой от 1 до 3 степень важности заметки\n'
                              ' 1 - высокая степень важности\n'
                              ' 2 - средняя степень важности\n'
                              ' 3 - низкая степень важности\n'
                              '>> ')
            if int(relevance) != 1 and int(relevance) != 2 and int(relevance) != 3:
                print('\nВы ввели неверную команду')

            else:
                if int(relevance) == 1:
                    relevance = 'Высокая'
                elif int(relevance) == 2:
                    relevance = 'Средняя'
                elif int(relevance) == 3:
                    relevance = 'Низкая'
            file.write('Важность = ' + relevance + '間')
            file.write('Создана = ' + datetime.now().strftime('%d-%m-%Y %H:%M:%S') + '間終\n')
            break



def note_list(user):
    """
    Функция по выводу списка заметок пользователя, принимает параметр user(авторизованного пользователя).
    :param user:str
    :return: None
    """
    try:
        with open(path_user + '\\' + user + '\\' + 'note_' + user + '.txt', 'r', encoding='utf-8') as file:
            notes = file.read()
            notes = notes.replace('間', ';\n').replace('終', '')
            print(notes)
    except FileNotFoundError:
        note_list_text()

    if os.path.isfile(path_user + '\\' + user + '\\' + 'note_' + user + '.txt'):
        search_file = open(path_user + '\\' + user + '\\' + 'note_' + user + '.txt', 'r', encoding='utf-8')
        search_point = '終'
        search_text = search_file.read()
        search_file.close()
        if search_point not in search_text:
            note_list_text()



def del_note(user):
    """
    Функция по удалению заметки пользователя, принимает параметр user(авторизованного пользователя).
    Выполняются следующие проверки:
    1) Наличие заметок у пользователя;
    2) Наличие конкретной заметки у пользователя.
    :param user: str
    :return: None.
    """
    while True:
        if not os.path.isfile(path_user + '\\' + user + '\\' + 'note_' + user + '.txt'):
            del_note_text_1()
            return False

        if os.path.isfile(path_user + '\\' + user + '\\' + 'note_' + user + '.txt'):
            search_file = open(path_user + '\\' + user + '\\' + 'note_' + user + '.txt', 'r', encoding='utf-8')
            search_point = '終'
            search_text = search_file.read()
            search_file.close()
            if search_point not in search_text:
                del_note_text_1()
                return False

        note_for_del = input('Введите номер заметки для удаления\n'
                             'Или break для выхода в предыдущее меню >> ')

        file = open(path_user + '\\' + user + '\\' + 'note_' + user + '.txt', 'r', encoding='utf-8')
        search_note = 'Заметка № ' + note_for_del
        text = file.read()
        file.close()
        if search_note in text:
            del_note_text_3()
            while True:
                confirmation = input('Ваша команда (введите no для выхода в предыдущее меню) >> ')
                if confirmation == 'yes':
                    with open(path_user + '\\' + user + '\\' + 'note_' + user + '.txt', 'r',encoding='utf-8') as old_file:
                        with open(path_user + '\\' + user + '\\' + '$note_' + user + '.txt', 'w', encoding='utf-8') as new_file:
                            for line in old_file:
                                if not line.strip('\n').startswith(search_note):
                                    new_file.write(line)
                    os.remove(path_user + '\\' + user + '\\' + 'note_' + user + '.txt')
                    os.rename(path_user + '\\' + user + '\\' + '$note_' + user + '.txt', path_user + '\\' + user + '\\' + 'note_' + user + '.txt')
                    del_note_text_4()
                    return False
                elif confirmation == 'no':
                    return False
                else:
                    error_input_1()
                    return False



        elif note_for_del == 'break' or note_for_del == 'Break':
            return False

        elif note_for_del == '':
            del_note_text_2()
            return False

        elif search_note not in text:
            del_note_text_5()
            return False

        else:
            error_input_1()
            return False


def find_note(user):
    """
    Функция по поиску заметки пользователя, принимает параметр user(авторизованного пользователя).
    Выполняются следующие проверки:
    1) Наличие заметок у пользователя;
    2) Наличие конкретной заметки у пользователя.
    :param user: str
    :return: None.
    """
    while True:
        if not os.path.isfile(path_user + '\\' + user + '\\' + 'note_' + user + '.txt'):
            find_note_text_1()
            return False
        if os.path.isfile(path_user + '\\' + user + '\\' + 'note_' + user + '.txt'):
            search_file = open(path_user + '\\' + user + '\\' + 'note_' + user + '.txt', 'r', encoding='utf-8')
            search_point = '終'
            search_text = search_file.read()
            search_file.close()
            if search_point not in search_text:
                find_note_text_1()
                return False

            note_for_find = input('Введите текст для поиска заметки\n'
                                 'Или break для выхода в предыдущее меню >> ')

            file = open(path_user + '\\' + user + '\\' + 'note_' + user + '.txt', 'r', encoding='utf-8')
            search_note = note_for_find
            text = file.read()
            file.close()
            if search_note in text:
                with open(path_user + '\\' + user + '\\' + 'note_' + user + '.txt', 'r',encoding='utf-8') as search_file:
                    with open(path_user + '\\' + user + '\\' + '$note_' + user + '.txt', 'w',encoding='utf-8') as buff_file:
                        for line in search_file:
                            if search_note in line.strip('\n'):
                                buff_file.write(line)
                with open(path_user + '\\' + user + '\\' + '$note_' + user + '.txt', 'r',encoding='utf-8') as buff_1_file:
                    find_text = buff_1_file.read()
                    find_text = find_text.replace('間', ';\n').replace('終', '')
                    print(find_text)
                os.remove(path_user + '\\' + user + '\\' + '$note_' + user + '.txt')


            elif note_for_find == 'break' or note_for_find == 'Break':
                return False

            elif note_for_find == '':
                find_note_text_2()
                return False

            elif search_note not in text:
                find_note_text_3()
                return False

            else:
                error_input_1()
                return False



def edit_note(user):
    """
    Функция по редактированию заметки (наименования, содержания и важности) пользователя, принимает параметр user(авторизованного пользователя).
    Выполняются следующие проверки:
    1) Наличие заметок у пользователя;
    2) Наличие конкретной заметки у пользователя.
    :param user: str
    :return: None.
    """
    while True:
        if not os.path.isfile(path_user + '\\' + user + '\\' + 'note_' + user + '.txt'):
            edit_note_text_1()
            return False
        if os.path.isfile(path_user + '\\' + user + '\\' + 'note_' + user + '.txt'):
            search_file = open(path_user + '\\' + user + '\\' + 'note_' + user + '.txt', 'r', encoding='utf-8')
            search_point = '終'
            search_text = search_file.read()
            search_file.close()
            if search_point not in search_text:
                edit_note_text_1()
                return False

        note_for_edit = input('Введите номер заметки для редактирования\n'
                             'Или break для выхода в предыдущее меню >> ')

        file = open(path_user + '\\' + user + '\\' + 'note_' + user + '.txt', 'r', encoding='utf-8')
        search_note = 'Заметка № ' + note_for_edit
        text = file.read()
        file.close()

        if note_for_edit == '':
            edit_note_text_2()
            return False

        if search_note in text:
            new_title_user = input('Введите новое название заметки >> ')
            new_text_user = input('Введите новое содержание заметки >> ')
            while True:
                relevance = input('Укажите цифрой от 1 до 3 степень важности заметки\n'
                                  ' 1 - высокая степень важности\n'
                                  ' 2 - средняя степень важности\n'
                                  ' 3 - низкая степень важности\n'
                                  '>> ')
                if int(relevance) != 1 and int(relevance) != 2 and int(relevance) != 3:
                    print('\nВы ввели неверную команду')

                else:
                    if int(relevance) == 1:
                        relevance = 'Высокая'
                    elif int(relevance) == 2:
                        relevance = 'Средняя'
                    elif int(relevance) == 3:
                        relevance = 'Низкая'
                edit_text = search_note + '間' + 'Наименование = ' + new_title_user + '間' + 'Содержание = ' + new_text_user + '間' + 'Важность = ' + relevance + '間' + 'Создана = ' + datetime.now().strftime('%d-%m-%Y %H:%M:%S') + '間終\n'

                with open(path_user + '\\' + user + '\\' + 'note_' + user + '.txt', 'r', encoding='utf-8') as buff_file:
                    with open(path_user + '\\' + user + '\\' + '$note_' + user + '.txt', 'w', encoding='utf-8') as new_file:
                        for line in buff_file:
                            if not line.strip('\n').startswith(search_note):
                                new_file.write(line)
                os.remove(path_user + '\\' + user + '\\' + 'note_' + user + '.txt')
                os.rename(path_user + '\\' + user + '\\' + '$note_' + user + '.txt', path_user + '\\' + user + '\\' + 'note_' + user + '.txt')
                with open(path_user + '\\' + user + '\\' + 'note_' + user + '.txt', 'a', encoding='utf-8') as buff_1_file:
                    buff_1_file.write(edit_text)
                edit_note_text_4()
                return False

        elif note_for_edit == 'break' or note_for_edit == 'Break':
            return False

        elif search_note not in text:
            edit_note_text_3()
            return False

        else:
            error_input_1()
            return False


def check_password(user_authorization):
    """
    Функция вывода пароля конкретного пользователя, принимает параметр user_authorization(авторизованного пользователя).
    :param user_authorization: str
    :return: str
    """
    with open(path + '\\users.txt', 'r', encoding='utf-8') as file:
        with open(path + '\\$$users.txt', 'w', encoding='utf-8') as buff_file:
            for line in file:
                if user_authorization in line.strip('\n'):
                    buff_file.write(line)
    with open(path + '\\$$users.txt', 'r', encoding='utf-8') as read_file:
        check_user = read_file.read()
        check_user = check_user.split('間')
        user_password = check_user[1]
        user_password = user_password.replace('user_password:', '')
        return user_password



def import_note(user, quoting=None):
    try:
        with open(path_user + '\\' + user + '\\' + 'note_' + user + '.txt', 'r', encoding='utf-8') as file_txt:
            content = file_txt.read()
            content = content.replace('Заметка № ', '').replace('Наименование = ', '').replace('Содержание = ', '').replace('Создана = ', '').replace('Важность = ', '')
            content = content.replace('終', '').replace('\n', '')
            print(content)
            content = content.split('間')
            #content_1 = []
            #[content_1.extend(idx.split('終\n')) for idx in content]
            print(content)
            #print(content_1)
            #with open(path_user + '\\' + user + '\\' + 'note_' + user + '.csv', newline='', encoding='utf-8') as csv_file:
                #col = ['Номер заметки', 'Наименование', 'Содержание', 'Важность']
                #writer = csv.DictWriter(csv_file, fieldnames=col)
                #writer.writeheader()
                #writer.writerow(content)



    except FileNotFoundError:
        note_list_text()

    if os.path.isfile(path_user + '\\' + user + '\\' + 'note_' + user + '.txt'):
        search_file = open(path_user + '\\' + user + '\\' + 'note_' + user + '.txt', 'r', encoding='utf-8')
        search_point = '終'
        search_text = search_file.read()
        search_file.close()
        if search_point not in search_text:
            note_list_text()



def main():
    """
    Основные функции по запуску приложения.
    :return: None.
    """
    enter_point()
    user_select()