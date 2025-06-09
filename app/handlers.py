import logging
from aiogram import Dispatcher, types, F
from aiogram.filters import Command
from langdetect import detect, LangDetectException
from llm import check_text_by_YApi
from chat_storage import save_enabled_chats, load_enabled_chats

logger = logging.getLogger(__name__)

# Load enabled chat IDs from storage (use a set for easy add/remove)
try:
    enabled_chats = set(load_enabled_chats())
except Exception:
    enabled_chats = set()

async def on_message(message: types.Message) -> None:
    # Only process text messages in group chats where the bot is enabled

    text = message.text 
    logger.info(text)

    logger.info(f"Received message {message.message_id} from {message.from_user.id} in chat {message.chat.id}")
        
    is_correct, answer = await check_text_by_YApi(text)
    if not is_correct:
        logger.info(f"Sending correction reply to message {message.message_id}")
        try:
            await message.reply(
                answer,
                reply_to_message_id=message.message_id
            )
            logger.info(f"Reply sent for message {message.message_id}")
        except Exception as e:
            logger.error(f"Failed to send reply: {e}")

async def enable_bot(message: types.Message) -> None:
    """Enable the bot in the current chat"""
    if message.chat.type == 'private':
        await message.reply("This command can only be used in group chats.")
        return

    chat_id = message.chat.id
    if chat_id not in enabled_chats:
        enabled_chats.add(chat_id)
        save_enabled_chats(list(enabled_chats))
        await message.reply(f"Bot has been enabled in this chat. Chat ID: {chat_id}")
    else:
        await message.reply(f"Bot is already enabled in this chat. Chat ID: {chat_id}")

async def disable_bot(message: types.Message) -> None:
    """Disable the bot in the current chat"""
    if message.chat.type == 'private':
        await message.reply("This command can only be used in group chats.")
        return

    chat_id = message.chat.id
    if chat_id in enabled_chats:
        enabled_chats.remove(chat_id)
        save_enabled_chats(list(enabled_chats))
        await message.reply(f"Bot has been disabled in this chat. Chat ID: {chat_id}")
    else:
        await message.reply(f"Bot is already disabled in this chat. Chat ID: {chat_id}")

async def get_chat_id(message: types.Message) -> None:
    """Get the current chat ID and status"""
    chat_id = message.chat.id
    chat_type = message.chat.type
    status = 'Yes' if chat_id in enabled_chats else 'No'
    await message.reply(
        f"Chat ID: {chat_id}\n"  
        f"Chat type: {chat_type}\n"
        f"Bot enabled: {status}"
    )


def register_handlers(dp: Dispatcher) -> None:
    # Message handler for enabled group chats
    dp.message.register(
        on_message,
        F.text
    )
