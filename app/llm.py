# app/llm.py
import aiohttp
import logging
import json
from yandex_cloud_ml_sdk import YCloudML
from yandex_cloud_ml_sdk.search_indexes import (
    HybridSearchIndexType,
    TextSearchIndexType,
    StaticIndexChunkingStrategy,
    ReciprocalRankFusionIndexCombinationStrategy,
)
from config import config

logger = logging.getLogger(__name__)

async def check_text_by_YApi(text: str) -> tuple[bool, str] | None:
    logger.info(f"LLM check for text: {text}")
    prompt = (
        "Ты — ассистент по проверке и исправлению сообщений на английском. "
        "Твоя задача принимать на вход любое предложение на английском, проверять его на грамматические и лексические\n"
        "Игнорируй ошибки связанные с пунктуацией, орфографией, мелкими грамматическими ошибками.\n"
        "Обращай внимание только на грубые ошибки, не говори о мелких ошибках.\n\n"
        "### Инструкция ###\n"
        "Если предлоежение не на английском, ответит:\n"
        "Ошибок не найдено\n\n"
        "Если ошибок нет, ответит:\n"
        "Ошибок не найдено\n\n"
        "Если есть одна ошибки есть:\n"
        "Правильный вариант: <правильный_вариант>\n"
        "Объяснение (на русском): <объяснение>\n\n"
        "Если есть несколько ошибок есть:\n"
        "Правильный вариант: <правильный_вариант>\n"
        "Объяснение(на русском): <объяснение_первый ошибки>\n"
        "<объяснение_второй_ошибки>\n\n"
        f"Текст для проверки:\n{text}"
    )
    message = "".join(prompt)
    print(message)

    sdk = YCloudML(
        folder_id="b1g02g6dkgm7a99v4vvg",
        auth="y0__xDJhMuwAxjB3RMgz9WamRKYPlTR_XgNODm7ycZ1rPvVG3r7kQ",
    )

    model = sdk.models.completions("yandexgpt")
    model = model.configure(temperature=0.5)
    text_data = model.run(prompt)
    text_data = text_data.alternatives[0].text

    is_correct = False
    answer = text_data.replace('Объяснение (на русском):', '')
    logger.info(text_data)
    if 'Ошибок не найдено' in answer:
        is_correct = True
    
        
    return is_correct, answer

