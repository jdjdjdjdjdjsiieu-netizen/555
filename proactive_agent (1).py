import asyncio
import os
from pyrogram import Client
from agent_core import generate_referral_message

# --- Конфигурация ---
# ВНИМАНИЕ: Для работы необходимо получить API_ID и API_HASH на my.telegram.org
# и установить их в переменные окружения.
# Пример: export TG_API_ID=1234567
# Пример: export TG_API_HASH="YOUR_API_HASH"
API_ID = os.environ.get("TG_API_ID")
API_HASH = os.environ.get("TG_API_HASH")
TARGET_CONTACTS = [
    # ВНИМАНИЕ: Замените на реальные юзернеймы или ID контактов, с которыми вы хотите общаться.
    # В реальном приложении этот список будет динамически формироваться.
    {"username": "user1_telegram_username", "info": "Имя: Иван, Интересы: Python, Data Science, ищет работу."},
    {"username": "user2_telegram_username", "info": "Имя: Мария, Интересы: Фриланс, безопасность, облачные сервисы."},
    # Добавьте больше контактов
]

# --- Имитация отправки сообщения ---
async def get_chat_history(client: Client, username: str, limit: int = 10) -> str:
    """
    Извлекает последние сообщения из чата с контактом.
    """
    try:
        messages = []
        async for message in client.get_chat_history(username, limit=limit):
            # Форматируем сообщение для передачи в LLM
            sender = "Я" if message.from_user.is_self else message.from_user.first_name
            messages.append(f"{sender}: {message.text}")
        
        # Возвращаем историю в обратном порядке (от старых к новым)
        return "\n".join(messages[::-1])
    except Exception as e:
        print(f"Ошибка при получении истории чата с {username}: {e}")
        return "История чата недоступна."

async def send_proactive_message(client: Client, username: str, message: str):
    """
    Отправляет сгенерированное сообщение контакту.
    """
    try:
        await client.send_message(username, message)
        print(f"Сообщение успешно отправлено контакту @{username}")
    except Exception as e:
        print(f"Ошибка при отправке сообщения контакту @{username}: {e}")

async def run_proactive_agent():
    """
    Основная функция агента:
    1. Инициализирует Pyrogram Client (User API).
    2. Проходит по списку целевых контактов.
    3. Извлекает историю чата.
    4. Генерирует персонализированное сообщение.
    5. Отправляет сообщение.
    """
    if not API_ID or not API_HASH:
        print("ОШИБКА: Не установлены переменные окружения TG_API_ID и TG_API_HASH.")
        print("Запуск реального агента невозможен. Запускается демонстрация логики.")
        
        # Демонстрация логики без реального клиента
        for contact in TARGET_CONTACTS:
            # Имитируем историю чата, если она не задана
            chat_history = contact.get("history", "История чата недоступна.")
            contact_info = contact["info"]
            
            referral_message = generate_referral_message(contact_info, chat_history)
            
            print(f"\n--- Демонстрация генерации для @{contact['username']} ---")
            print(f"Контекст: {contact_info}")
            print(f"История чата: {chat_history}")
            print(f"Сгенерированное сообщение:\n{referral_message}")
            print("-------------------------------------------------------")
        
        print("\nПроактивный цикл завершен (Демонстрация).")
        return

    print("Запуск проактивного агента (Реальный режим)...")
    
    # Инициализация клиента Pyrogram (User API)
    # 'my_account' - это имя сессии. При первом запуске запросит код авторизации.
    client = Client("my_account", api_id=int(API_ID), api_hash=API_HASH)
    
    async with client:
        print("Клиент Pyrogram авторизован.")
        
        for contact in TARGET_CONTACTS:
            username = contact["username"]
            contact_info = contact["info"]
            
            # 1. Извлечение реальной истории чата
            chat_history = await get_chat_history(client, username)
            
            # 2. Генерация персонализированного реферального сообщения
            referral_message = generate_referral_message(contact_info, chat_history)
            
            # 3. Отправка сообщения
            await send_proactive_message(client, username, referral_message)

    print("\nПроактивный цикл завершен.")

if __name__ == "__main__":
    print("--- Проактивный агент Telegram ---")
    asyncio.run(run_proactive_agent())

# --- Основная логика проактивного агента ---
async def run_proactive_agent():
    """
    Основная функция агента:
    1. Инициализирует Pyrogram Client (User API).
    2. Проходит по списку целевых контактов.
    3. Генерирует персонализированное сообщение для каждого контакта.
    4. Имитирует отправку сообщения.
    """
    print("Запуск проактивного агента...")
    
    # Инициализация клиента Pyrogram (User API)
    # 'my_account' - это имя сессии, которое будет использоваться для хранения данных авторизации
    # В реальном приложении, при первом запуске, Pyrogram запросит код авторизации
    # Для демонстрации мы не будем запускать реальный клиент, а только имитируем логику
    

