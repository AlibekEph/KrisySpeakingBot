# app/main.py
import logging
import asyncio
from logging import FileHandler, Formatter, StreamHandler
from aiogram import Bot, Dispatcher
from config import config
from handlers import register_handlers

async def main():
    # Configure logging: file and console handlers
    log_file = config.logging['file']
    level = getattr(logging, config.logging['level'].upper(), logging.INFO)
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # File handler
    file_handler = FileHandler(log_file)
    file_handler.setLevel(level)
    file_formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    
    # Console handler
    console_handler = StreamHandler()
    console_handler.setLevel(level)
    console_formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    
    # Add handlers
    root_logger.handlers = [file_handler, console_handler]

    logger = logging.getLogger(__name__)
    logger.info("Starting Telegram bot")

    bot = Bot(token=config.telegram['token'])
    dp = Dispatcher()
    register_handlers(dp)
    try:
        await dp.start_polling(bot, skip_updates=True)
    except Exception as e:
        logger.exception(f"Polling failed: {e}")

if __name__ == '__main__':
    asyncio.run(main())
