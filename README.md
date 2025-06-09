# KristyBot - English Grammar Checker Bot

Telegram бот для проверки грамматики английского языка в групповых чатах. Бот использует YandexGPT для анализа текста и предоставляет исправления с объяснениями на русском языке.

## Требования

- Python 3.10 или выше
- Docker (опционально, для запуска в контейнере)
- Telegram Bot Token (получить у [@BotFather](https://t.me/BotFather))
- Доступ к YandexGPT API

## Установка и запуск

### Вариант 1: Локальный запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/KristyBot.git
cd KristyBot
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
# или
.\venv\Scripts\activate  # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Настройте конфигурацию:
```bash
cp settings.ini-example settings.ini
```
Отредактируйте `settings.ini` и заполните необходимые параметры:
- `token` - токен вашего Telegram бота
- `url` - URL вашего LLM API
- `model` - название модели для использования

5. Запустите бота:
```bash
python app/main.py
```

### Вариант 2: Запуск в Docker

1. Соберите Docker образ:
```bash
docker build -t kristybot .
```

2. Настройте конфигурацию:
```bash
cp settings.ini-example settings.ini
```
Отредактируйте `settings.ini` как описано выше.

3. Запустите контейнер:
```bash
docker-compose up -d
```

## Использование

1. Добавьте бота в групповой чат
2. Используйте команды:
   - `/enable` - включить бота в текущем чате
   - `/disable` - отключить бота в текущем чате
   - `/chatid` - получить ID чата и статус бота

3. Бот будет автоматически проверять английские сообщения в чате и отвечать с исправлениями, если найдет ошибки.

## Формат ответов бота

Если ошибок нет:
```
Ошибок не найдено
```

Если есть ошибки:
```
Правильный вариант: <исправленный_текст>
Объяснение (на русском): <подробное_объяснение_ошибок>
```

## Логирование

Логи сохраняются в файл `bot.log`. Уровень логирования можно настроить в `settings.ini`:
- DEBUG - подробная отладочная информация
- INFO - основная информация о работе бота
- WARNING - предупреждения
- ERROR - ошибки
- CRITICAL - критические ошибки

## Структура проекта

```
KristyBot/
├── app/
│   ├── __init__.py
│   ├── main.py          # Основной файл бота
│   ├── handlers.py      # Обработчики команд
│   ├── llm.py          # Интеграция с LLM API
│   └── config.py       # Конфигурация
├── settings.ini        # Конфигурационный файл (не в git)
├── settings.ini-example # Пример конфигурации
├── requirements.txt    # Зависимости Python
├── Dockerfile         # Конфигурация Docker
├── docker-compose.yaml # Конфигурация Docker Compose
└── README.md          # Этот файл
```

## Лицензия

MIT License 