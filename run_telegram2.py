import os
from dotenv import load_dotenv
from telegram import Bot
import asyncio

def send_test_message():
    load_dotenv()
    token = os.getenv('TELEGRAM_TOKEN')
    channel_id = os.getenv('TELEGRAM_CHANNEL_ID')
     print(f'token: {token}, channel_id: {channel_id}')
    if not token or not channel_id:
        print('TELEGRAM_TOKEN или TELEGRAM_CHANNEL_ID не заданы в .env')
        return
    bot = Bot(token=token)
    async def main():
        try:
            await bot.send_message(chat_id=channel_id, text='Тестовое сообщение от бота!')
            print('Тестовое сообщение отправлено!')
        except Exception as e:
            print(f'Ошибка при отправке: {e}')
    asyncio.run(main())

if __name__ == "__main__":
    send_test_message() 