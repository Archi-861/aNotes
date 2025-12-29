from __future__ import annotations


import csv
import json
from datetime import datetime, date
from pathlib import Path


BASE_DIR = Path('data')
USERS_DIR = BASE_DIR / 'users'



def ensure_storage():
    USERS_DIR.mkdir(parents=True, exist_ok=True)



def user_file(username: str):
    return USERS_DIR / f'{username}.txt'



def list_users():
    ensure_storage()
    return sorted([p.stem for p in USERS_DIR.glob('*.txt')])



def user_exists(username: str):
    ensure_storage()
    return user_file(username).exists()



def create_user(username: str):
    ensure_storage()
    username = username.strip()
    if not username:
        raise ValueError('Имя пользователя не может быть пустым.')

    path = user_file(username)
    if path.exists():
        raise ValueError('Пользователь уже существует.')
    path.write_text('', encoding='utf-8')



def rename_user(old_name: str, new_name: str):
    ensure_storage()
    old_name = old_name.strip()
    new_name = new_name.strip()

    if not old_name or not new_name:
        raise ValueError('Имя не может быть пустым.')
    old_path = user_file(old_name)
    new_path = user_file(new_name)

    if not old_path.exists():
        raise ValueError('Пользователь не найден.')
    if new_path.exists():
        raise ValueError('Новое имя уже занято.')
    old_path.rename(new_path)



def delete_user(username: str):
    ensure_storage()
    path = user_file(username)
    if path.exists():
        path.unlink()



def load_notes(username: str):
    path = user_file(username)
    if not path.exists():
        return []

    notes: list[dict] = []
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            notes.append(json.loads(line))
        except json.JSONDecodeError:
            continue

    normalized, changed = normalize_notes(notes)
    if changed:
        save_notes(username, normalized)
    return normalized



def save_notes(username: str, notes: list[dict]):
    path = user_file(username)
    lines = [json.dumps(n, ensure_ascii=False) for n in notes]
    content = '\n'.join(lines)
    if content:
        content += '\n'
    path.write_text(content, encoding='utf-8')



def get_next_note_id(notes: list[dict]):
    ids = [n.get('id') for n in notes if isinstance(n.get('id'), int)]
    return (max(ids) + 1) if ids else 1



def new_note(username: str, title: str, content: str, importance: int, existing_notes: list[dict]):
    return {
        'id': get_next_note_id(existing_notes),
        'title': title.strip(),
        'content': content.strip(),
        'importance': importance,  # 1/2/3
        'owner': username,
        'created_at': datetime.now().isoformat(timespec='seconds'),
    }



def add_note(username: str, note: dict):
    notes = load_notes(username)
    notes.append(note)
    save_notes(username, notes)


def find_notes_by_title(username: str, query: str):
    query = query.strip().lower()
    return [n for n in load_notes(username) if query in str(n.get('title', '')).lower()]



def delete_note(username: str, note_id: int):
    notes = load_notes(username)
    new_notes = [n for n in notes if n.get('id') != note_id]
    if len(new_notes) == len(notes):
        return False
    save_notes(username, new_notes)
    return True



def update_note(username: str, note_id: int, updates: dict):
    notes = load_notes(username)
    for n in notes:
        if n.get('id') == note_id:
            n.update(updates)
            save_notes(username, notes)
            return True
    return False



def normalize_notes(notes: list[dict]):
    changed = False
    normalized: list[dict] = []

    need_renumber = any(not isinstance(n.get('id'), int) for n in notes)

    if need_renumber:
        changed = True
        next_id = 1
        for n in notes:
            item = dict(n)
            item['id'] = next_id
            item['importance'] = _normalize_importance(item.get('importance'))
            normalized.append(item)
            next_id += 1
        return normalized, changed

    for n in notes:
        item = dict(n)
        old_imp = item.get('importance')
        new_imp = _normalize_importance(old_imp)
        if new_imp != old_imp:
            changed = True
        item['importance'] = new_imp
        normalized.append(item)

    return normalized, changed



def _normalize_importance(value):
    try:
        v = int(value)
    except Exception:
        return 1
    if v in (1, 2, 3):
        return v
    return 1



def parse_day(day_str: str):
    return datetime.strptime(day_str, '%Y-%m-%d').date()



def filter_by_day(notes: list[dict], day_str: str):
    target = parse_day(day_str)
    result: list[dict] = []
    for n in notes:
        try:
            created = datetime.fromisoformat(str(n.get('created_at', ''))).date()
        except Exception:
            continue
        if created == target:
            result.append(n)
    return result



def default_export_path(username: str):
    downloads = Path.home() / 'Downloads'
    if downloads.exists() and downloads.is_dir():
        return downloads / f'{username}_notes.csv'

    exports = BASE_DIR / 'exports'
    exports.mkdir(parents=True, exist_ok=True)
    return exports / f'{username}_notes.csv'



def export_notes_to_csv(username: str, csv_path: Path):
    notes = load_notes(username)
    with csv_path.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(
            f,
            fieldnames=['id', 'title', 'content', 'importance', 'owner', 'created_at'],
        )
        writer.writeheader()
        for n in notes:
            writer.writerow({
                'id': n.get('id'),
                'title': n.get('title'),
                'content': n.get('content'),
                'importance': n.get('importance'),
                'owner': n.get('owner'),
                'created_at': n.get('created_at'),
            })


def export_notes_to_default_csv(username: str):
    ensure_storage()
    path = default_export_path(username)
    export_notes_to_csv(username, path)
    return str(path)
