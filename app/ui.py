from __future__ import annotations


from app import services


def run_app():
    while True:
        print('\n=== ANotes ===')
        print('1) Пользователи')
        print('2) Заметки')
        print('0) Выход')
        print('\n© All karas reserved')

        cmd = input('-> ').strip()

        if cmd == '1':
            users_menu()
        elif cmd == '2':
            print('Сначала выбери пользователя: Пользователи -> Войти как пользователь.')
        elif cmd == '0':
            print('Пока!')
            return
        else:
            print('Неизвестная команда. Kara!')



def users_menu():
    while True:
        print('\n=== Пользователи ===')
        print('1) Список пользователей')
        print('2) Создать пользователя')
        print('3) Переименовать пользователя')
        print('4) Удалить пользователя')
        print('5) Войти как пользователь')
        print('0) Назад')

        cmd = input('-> ').strip()

        if cmd == '1':
            users = services.get_users()
            if not users:
                print('Пользователей нет.')
            else:
                for u in users:
                    print('-', u)

        elif cmd == '2':
            print('Введите имя пользователя (0 — отмена)')
            name = input('>> ').strip()
            if name == '0':
                print('Отмена.')
                continue
            try:
                services.create_new_user(name)
                print('Пользователь создан.')
            except (ValueError, OSError) as e:
                print('Ошибка:', e)

        elif cmd == '3':
            old_name = input('Старое имя (0 — отмена): ').strip()
            if old_name == '0':
                continue
            new_name = input('Новое имя (0 — отмена): ').strip()
            if new_name == '0':
                continue
            try:
                services.rename_existing_user(old_name, new_name)
                print('Пользователь переименован.')
            except (ValueError, OSError) as e:
                print('Ошибка:', e)

        elif cmd == '4':
            name = input('Имя пользователя для удаления (0 — отмена): ').strip()
            if name == '0':
                continue
            if not services.check_user(name):
                print('Такого пользователя нет.')
                continue

            confirm = input(f'Точно удалить \'{name}\' и все его заметки? (yes/no): ').strip().lower()
            if confirm == 'yes':
                try:
                    services.remove_user(name)
                    print('Пользователь удалён.')
                except OSError as e:
                    print('Ошибка:', e)
            else:
                print('Удаление отменено.')

        elif cmd == '5':
            username = input('Имя пользователя (0 — отмена): ').strip()
            if username == '0':
                continue
            if not services.check_user(username):
                print('Такого пользователя нет.')
                continue
            notes_menu(username)

        elif cmd == '0':
            return
        else:
            print('Неизвестная команда. Kara!')



def print_note(n: dict):
    mark = {1: '[!]', 2: '[!!]', 3: '[!!!]'}.get(n.get('importance'), '[?]')
    print(f'{mark} {n.get("id")} | {n.get("title")} | {n.get("created_at")}')
    print(f'    {n.get("content")}')



def input_importance(allow_empty: bool = False):
    while True:
        prompt = 'Важность: 1-низкая, 2-средняя, 3-высокая'
        if allow_empty:
            prompt += ' (пусто — не менять)'
        prompt += ' (0 — отмена): '
        s = input(prompt).strip()
        if s == '0':
            return '0'
        if allow_empty and s == '':
            return None
        if s in ('1', '2', '3'):
            return int(s)
        print('Неверно. Введите 1/2/3.')



def input_note_id():
    s = input('ID заметки (0 — отмена): ').strip()
    if s == '0':
        return None
    if not s.isdigit():
        print('ID должен быть числом.')
        return None
    return int(s)



def notes_menu(username: str):
    while True:
        print(f'\n=== Заметки пользователя: {username} ===')
        print('1) Добавить заметку')
        print('2) Показать все заметки')
        print('3) Найти по названию')
        print('4) Редактировать заметку по id')
        print('5) Удалить заметку по id')
        print('6) Сортировка (1-дата, 2-название, 3-важность)')
        print('7) Фильтр (день и/или важность)')
        print('8) Экспорт в CSV (в Downloads)')
        print('0) Назад')
        cmd = input('-> ').strip()

        if cmd == '1':
            title = input('Наименование (0 — отмена): ').strip()
            if title == '0':
                continue
            if not title:
                print('Название не может быть пустым.')
                continue

            content = input('Содержание (0 — отмена): ').strip()
            if content == '0':
                continue
            if not content:
                print('Содержание не может быть пустым.')
                continue

            importance = input_importance()
            if importance == '0':
                continue

            try:
                services.create_note(username, title, content, importance)
                print('Заметка добавлена.')
            except OSError as e:
                print('Ошибка:', e)

        elif cmd == '2':
            notes = services.get_notes(username)
            if not notes:
                print('Заметок нет.')
            else:
                for n in notes:
                    print_note(n)

        elif cmd == '3':
            q = input('Введите часть названия (0 — отмена): ').strip()
            if q == '0':
                continue
            res = services.search_notes(username, q)
            if not res:
                print('Ничего не найдено.')
            else:
                for n in res:
                    print_note(n)

        elif cmd == '4':
            note_id = input_note_id()
            if note_id is None:
                continue

            print('Оставь поле пустым, если не хочешь менять.')
            title = input('Новое наименование: ').strip()
            content = input('Новое содержание: ').strip()
            importance = input_importance(allow_empty=True)
            if importance == '0':
                continue

            updates = {}
            if title:
                updates['title'] = title
            if content:
                updates['content'] = content
            if importance is not None:
                updates['importance'] = importance

            if not updates:
                print('Нечего обновлять.')
                continue

            ok = services.edit_note(username, note_id, updates)
            print('Обновлено.' if ok else 'Заметка не найдена.')

        elif cmd == '5':
            note_id = input_note_id()
            if note_id is None:
                continue
            ok = services.remove_note(username, note_id)
            print('Удалено.' if ok else 'Заметка не найдена.')

        elif cmd == '6':
            raw = input('Сортировка: 1-дата, 2-название, 3-важность (0 — отмена): ').strip().lower()
            if raw == '0':
                continue

            mode_map = {'1': 'date', '2': 'title', '3': 'importance'}
            mode = mode_map.get(raw)
            if not mode:
                print('Неверный выбор. Kara!')
                continue

            try:
                notes = services.get_notes(username)
                sorted_notes = services.sort_notes(notes, mode)
                if not sorted_notes:
                    print('Заметок нет.')
                else:
                    for n in sorted_notes:
                        print_note(n)
            except ValueError as e:
                print('Ошибка:', e)

        elif cmd == '7':
            day = input('День (YYYY-MM-DD) или пусто (0 — отмена): ').strip()
            if day == '0':
                continue

            imp_raw = input('Важность (1/2/3) или пусто: ').strip()
            importance = None
            if imp_raw:
                if imp_raw not in ('1', '2', '3'):
                    print('Неверная важность.')
                    continue
                importance = int(imp_raw)

            notes = services.get_notes(username)
            try:
                filtered = services.filter_notes(
                    notes,
                    importance=importance,
                    day=day if day else None,
                )
            except ValueError:
                print('Неверный формат даты. Нужно YYYY-MM-DD, например 2025-12-26.')
                continue

            if not filtered:
                print('Ничего не найдено.')
            else:
                for n in filtered:
                    print_note(n)

        elif cmd == '8':
            try:
                path = services.export_csv_default(username)
                print(f'Экспортировано в: {path}')
            except OSError as e:
                print('Ошибка экспорта:', e)

        elif cmd == '0':
            return
        else:
            print('Неизвестная команда. Kara!')
