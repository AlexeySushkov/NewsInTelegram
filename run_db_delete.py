import sqlite3
import os

DB_PATH = 'news.db'

def close_and_delete_db():
    # Попытка закрыть соединение, если оно открыто
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.close()
    except Exception:
        pass
    # Удаление файла базы данных
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Файл {DB_PATH} удалён.")
    else:
        print(f"Файл {DB_PATH} не найден.")

if __name__ == "__main__":
    close_and_delete_db() 