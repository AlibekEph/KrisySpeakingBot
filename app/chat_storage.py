# app/chat_storage.py
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

STORAGE_FILE = Path("enabled_chats.json")

def save_enabled_chats(enabled_chats: set[int]) -> None:
    """Save enabled chat IDs to a file"""
    try:
        with open(STORAGE_FILE, 'w') as f:
            json.dump(list(enabled_chats), f)
        logger.info(f"Saved {len(enabled_chats)} enabled chats to {STORAGE_FILE}")
    except Exception as e:
        logger.error(f"Failed to save enabled chats: {e}")

def load_enabled_chats() -> set[int]:
    """Load enabled chat IDs from a file"""
    try:
        if STORAGE_FILE.exists():
            with open(STORAGE_FILE, 'r') as f:
                chats = json.load(f)
            logger.info(f"Loaded {len(chats)} enabled chats from {STORAGE_FILE}")
            return set(chats)
    except Exception as e:
        logger.error(f"Failed to load enabled chats: {e}")
    return set() 