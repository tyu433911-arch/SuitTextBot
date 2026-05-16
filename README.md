# ОфициальныйТекст — Telegram-бот

Бот переводит обычный текст в официальный деловой стиль.

## Быстрый запуск

### 1. Получи ключи
- Telegram токен: [@BotFather](https://t.me/BotFather) → /newbot
- Gemini API ключ: [aistudio.google.com](https://aistudio.google.com) → Get API Key (бесплатно)

### 2. Локальный запуск
```bash
pip install -r requirements.txt
cp .env.example .env
# заполни .env своими ключами
python bot.py
```

### 3. Деплой на Railway
1. Загрузи проект на GitHub
2. railway.app → New Project → Deploy from GitHub
3. В Variables добавь TELEGRAM_TOKEN и GEMINI_API_KEY
4. Deploy — готово

## Лимиты бесплатного Gemini
- 15 запросов в минуту
- 1500 запросов в день
- Достаточно для валидации спроса
