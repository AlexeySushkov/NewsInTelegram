import os
from dotenv import load_dotenv
from telegram import Bot
from telegram.request import HTTPXRequest
import httpx
import asyncio

def send_test_message():
    load_dotenv()
    token = os.getenv('TELEGRAM_TOKEN')
    channel_id = os.getenv('TELEGRAM_CHANNEL_ID')
    if not token or not channel_id:
        print('TELEGRAM_TOKEN или TELEGRAM_CHANNEL_ID не заданы в .env')
        return
    # Временно отключаем SSL-проверку через кастомный httpx.AsyncClient
    client = httpx.AsyncClient(verify=False)
    request = HTTPXRequest(client=client)
    bot = Bot(token=token, request=request)
    async def main():
        try:
            await bot.send_message(chat_id=channel_id, text='Тестовое сообщение от бота!')
            print('Тестовое сообщение отправлено!')
        except Exception as e:
            print(f'Ошибка при отправке: {e}')
    asyncio.run(main())

if __name__ == "__main__":
    send_test_message() 