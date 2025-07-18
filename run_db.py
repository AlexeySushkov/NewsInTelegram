import sqlite3
from extract_links import extract_links
from filter_links import filter_links_by_substring
from get_html import get_html
import os
from dotenv import load_dotenv
from telegram import Bot
import asyncio

DB_PATH = 'news.db'


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            content TEXT UNIQUE,
            text TEXT
        )
    ''')
    conn.commit()
    conn.close()


def split_message(text, max_length=4096):
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]


async def send_to_telegram(text: str):
    load_dotenv()
    token = os.getenv('TELEGRAM_TOKEN')
    channel_id = os.getenv('TELEGRAM_CHANNEL_ID')
    if not token or not channel_id:
        print('TELEGRAM_TOKEN или TELEGRAM_CHANNEL_ID не заданы в .env')
        return
    bot = Bot(token=token)
    try:
        for part in split_message(text):
            await bot.send_message(chat_id=channel_id, text=part)
        print('Новость отправлена в Telegram')
    except Exception as e:
        print(f'Ошибка при отправке в Telegram: {e}')


def run():
    url = "https://techcrunch.com/2025/07/16/"
    links = extract_links(url)
    filtered_links = filter_links_by_substring(links, "2025/07/16")
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for news_url in filtered_links:
        c.execute("SELECT id FROM news WHERE content = ?", (news_url,))
        if c.fetchone() is None:
            try:
                text = get_html(news_url)
            except Exception as e:
                print(f"Ошибка при получении текста для {news_url}: {e}")
                continue
            try:
                c.execute("INSERT INTO news (url, content, text) VALUES (?, ?, ?)", (url, news_url, text))
                print(f"Добавлено: {news_url}")
                asyncio.run(send_to_telegram(text))
            except Exception as e:
                print(f"Ошибка при добавлении {news_url} в базу: {e}")
        else:
            print(f"Уже в базе: {news_url}")
    conn.commit()
    conn.close()
    print("DB closed")


if __name__ == "__main__":
    init_db()
    run() 