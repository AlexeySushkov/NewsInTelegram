import sqlite3
import os
import argparse
from dotenv import load_dotenv
import requests

DB_PATH = 'news.db'

PROMPT = (
    "Вот список новостей. Выбери 5 лучших и выведи их в виде списка. "
    "Если новостей меньше 5, выведи все. Не добавляй ничего лишнего. "
    "Сохрани оригинальный текст каждой новости.\n\n"
)

def get_news(filter_substring=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if filter_substring:
        c.execute("SELECT text FROM news WHERE content LIKE ?", (f"%{filter_substring}%",))
    else:
        c.execute("SELECT text FROM news")
    news = [row[0] for row in c.fetchall()]
    conn.close()
    return news

def ask_openrouter(news_list, model, api_key, api_url):
    prompt = PROMPT + '\n'.join(f"{i+1}. {n}" for i, n in enumerate(news_list))
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Ты — помощник, который выбирает лучшие новости."},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(f"{api_url}/chat/completions", json=data, headers=headers, verify=False)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Отправить новости через OpenRouter и выбрать 5 лучших.")
    parser.add_argument('--model', default=os.getenv('OPENROUTER_MODEL', 'deepseek-ai/deepseek-llm-67b-chat'), help='ID модели OpenRouter')
    parser.add_argument('--api_key', default=os.getenv('OPENROUTER_API_KEY'), help='API ключ OpenRouter')
    parser.add_argument('--api_url', default=os.getenv('OPENROUTER_API_URL', 'https://openrouter.ai/api/v1'), help='URL OpenRouter API')
    parser.add_argument('--filter', default=None, help='Фильтр для поиска новостей (по content)')
    args = parser.parse_args()

    if not args.api_key:
        print('API ключ не задан. Укажите через --api_key или переменную окружения OPENROUTER_API_KEY')
        return

    news = get_news(args.filter)
    if not news:
        print('Нет новостей по фильтру.')
        return
    print(f'Найдено новостей: {len(news)}')
    summary = ask_openrouter(news, args.model, args.api_key, args.api_url)
    print('\nЛучшие новости по версии LLM:\n')
    print(summary)

if __name__ == "__main__":
    main() 