from __future__ import annotations


import re
from app import storage


IMPORTANCE_ORDER = {1: 1, 2: 2, 3: 3}



def get_users():
    return storage.list_users()


def _validate_username(username: str):
    username = username.strip()
    if not re.fullmatch(r'[A-Za-zА-Яа-я0-9_-]{1,32}', username):
        raise ValueError('Имя: только буквы/цифры/_/-, длина 1..32')
    return username



def create_new_user(username: str):
    username = _validate_username(username)
    storage.create_user(username)



def rename_existing_user(old_name: str, new_name: str):
    old_name = _validate_username(old_name)
    new_name = _validate_username(new_name)
    storage.rename_user(old_name, new_name)



def remove_user(username: str):
    username = username.strip()
    storage.delete_user(username)


def check_user(username: str):
    return storage.user_exists(username)



def create_note(username: str, title: str, content: str, importance: int):
    notes = storage.load_notes(username)
    note = storage.new_note(username, title, content, importance, notes)
    storage.add_note(username, note)



def get_notes(username: str):
    return storage.load_notes(username)



def search_notes(username: str, query: str):
    return storage.find_notes_by_title(username, query)



def remove_note(username: str, note_id: int):
    return storage.delete_note(username, note_id)



def edit_note(username: str, note_id: int, updates: dict):
    return storage.update_note(username, note_id, updates)



def sort_notes(notes: list[dict], mode: str):
    mode = mode.strip().lower()
    if mode == 'date':
        return sorted(notes, key=lambda n: str(n.get('created_at', '')))

    if mode == 'title':
        return sorted(notes, key=lambda n: str(n.get('title', '')).lower())

    if mode == 'importance':
        return sorted(notes, key=lambda n: int(n.get('importance', 0)), reverse=True)

    raise ValueError('Неизвестный режим сортировки')



def filter_notes(notes: list[dict], importance: int | None = None, day: str | None = None):
    result = notes
    if importance is not None:
        result = [n for n in result if n.get('importance') == importance]

    if day:
        result = storage.filter_by_day(result, day)

    return result



def export_csv_default(username: str):
    return storage.export_notes_to_default_csv(username)
