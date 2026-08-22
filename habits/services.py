import os
import requests
from dotenv import load_dotenv

load_dotenv()


def send_telegram_message(chat_id: str, message: str) -> None:
    """Отправляет текстовое сообщение пользователю в Telegram."""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    print(f"[DEBUG] TELEGRAM_BOT_TOKEN present: {bool(bot_token)}, chat_id: {chat_id}")

    if not bot_token or not chat_id:
        print("[DEBUG] Пропуск отправки: отсутствует токен или chat_id")
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"[DEBUG] Telegram API response: status={response.status_code}, body={response.text}")
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Ошибка отправки сообщения в Telegram (chat_id: {chat_id}): {e}")
