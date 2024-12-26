import  os
from lower_logic import bold_text, create_directory, create_new_user, user_select_info, input_user_select


def enter_point():
    user_name = os.environ.get("USERNAME")
    print('Привет,' + bold_text(user_name) + '! \n'
          'Добро пожаловать в приложение aNotes!\n')



def user_select():
    user_name = os.environ.get("USERNAME")
    path = 'C:\\Users\\' + user_name + '\\Documents\\aNotes'
    create_directory()
    user_list = os.listdir(path)
    user_select_info()
    while True:
        var = input('Введите команду >> ')
        user_var = input_user_select(var)
        if user_var == 'exit':
            return False



