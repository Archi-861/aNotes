import  os

from support import *
import shutil


user_name = os.environ.get("USERNAME")
path = 'C:\\Users\\' + user_name + '\\Documents\\aNotes'
path_user = 'C:\\Users\\' + user_name + '\\Documents\\aNotes\\Users'

spec_symbol = '~$^№@[]{}<>=.,:;!_*-+()/#%&'


def note_date():
    time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    return time


def enter_point():
    print('Привет, ' + user_name + '! \n'
          'Добро пожаловать в приложение aNotes!\n')


def user_select():
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

        if user_var == 'exit':
            return False


'''
Функция обработки команд пользователя
'''

def input_user_select(var):
    user_list = os.listdir(path_user)

    if var == 'exit':
        return var

    elif var == 'list':
        if len(user_list) == 0:
            user_list_text()
            add_new_user()
            help_info()

        elif len(user_list) > 0:
            for user in user_list:
                print(user)
            help_info()

    elif var == 'add':
        add_new_user()
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
'''
Функция создания нового пользователя
'''

def add_new_user():
    while True:
        user = input('Введите имя пользователя, непревышающее 12 символов\n'
                     'Или введите break для выхода в предыдущее меню >> ')

        if user == '':
            add_new_user_text_1()
            continue

        if os.path.isdir(path_user + '\\' + user):
            add_new_user_text_2()
            continue

        if user == 'break':
            break

        if user == 'DELETED':
            add_new_user_text_1()
            continue

        if len(user) <= 12:
            os.mkdir(path_user + '\\' + user)
            new_path = path_user + '\\' + user
            with open(path + '\\users.txt', 'a', encoding='utf-8') as file:
                file.write('user_name:' + user + '間')
                file.write('user_path:' + new_path + '間\n')
                add_new_user_text_3()
                break

        else:
            error_input_2()


'''
Функция удаления пользователя
'''

def user_del():
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
                    break
                if confirmation == 'no':
                    help_info()
                    break


'''
Функция  выбора пользователя
'''

def user_login():
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
            add_note_menu()

            while  True:
                user = user_for_login
                action = input('Введите команду для заметок>> ')
                main_note(action, user)
                help_info_note()

                if action == 'exit':
                    return False




'''
Функция редактирования пользователя
'''

def user_edit():
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


'''
Функция вывода информация для последующего выбора команды пользователем
'''

def user_select_info():
    user_select_info_text()


'''
Функция вызова информации для помощи пользователю
'''

def help_info():
    help_info_text()


'''
Блок по заметкам
'''

def main_note(action, user):

    if action == 'exit':
        return False

    elif action == 'create':
        add_note(user)

    elif action == 'list':
        list_note(user)
        # if not os.path.isfile(path_user + '\\' + user + '\\note_' + user + '.txt'):
        #     note_list_text()
        # else:
        #     notes = os.listdir(path_user + '\\' + user)
        #     print(notes)
        #     for file in os.listdir(path_user + '\\' + user):
        #         print(file)
        #         if file.endswith('.txt'):
        #             print(file)
        #             with open(file, 'r', encoding='utf-8') as f:
        #                 line = f.readline()
        #                 print(line)

    elif action == 'del':
        del_note(user)

    elif action == 'help':
        add_note_menu()

    elif action == 'find':
        find_note(user)

    elif action == 'edit':
        edit_note(user)

def add_note(user):
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



def list_note(user):
    with open(path_user + '\\' + user + '\\' + 'note_' + user + '.txt', 'r', encoding='utf-8') as file:
        notes = file.read()
        notes = notes.replace('間', ';\n').replace('終', '')
        print(notes)


def del_note(user):
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


'''
Основные функции
'''
def main():
    enter_point()
    user_select()