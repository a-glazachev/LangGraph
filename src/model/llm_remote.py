"""
Module: model/llm_remote.py
Description:
    This module is responsible for interaction with remote LLM.
"""

from typing import Dict, Any, List

from langfuse.openai import openai

from src.model.variables import YC_API_KEY, YC_FOLDER_ID

TEMPERATURE = 0.2
MAX_TOKENS = 5000
MODEL = f"gpt://{YC_FOLDER_ID}/yandexgpt-lite"

client = openai.OpenAI(
    api_key=YC_API_KEY,
    base_url="https://ai.api.cloud.yandex.net/v1",
    project=YC_FOLDER_ID,
)


def invoke(system_prompt: str, user_prompt: str, node: str) -> Dict[str, Any]:
    messages = build_messages(system_prompt, user_prompt)
    return client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        stream=False,
        name=f"yandex-llm-{node}"
    )


def invoke_structured(system_prompt: str, user_prompt: str, result_class: Any, node: str) -> Dict[str, Any]:
    messages = build_messages(system_prompt, user_prompt)
    return client.chat.completions.parse(
        model=MODEL,
        messages=messages,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        response_format=result_class,
        name=f"yandex-llm-{node}"
    )


def build_messages(system_prompt: str, user_prompt: str) -> List[Dict[str, str]]:
    """
    Builds a list of messages for the GPT model based on the provided text.
    """
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
