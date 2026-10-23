"""
Module: model/llm_local.py
Description:
    This module is responsible for interaction with local LLM.
"""

from typing import Dict, Any, List

from langfuse.openai import openai

TEMPERATURE = 0.2
MAX_TOKENS = 10000
MODEL = "qwen3:4b"

client = openai.OpenAI(
    api_key="dummy",
    base_url="http://localhost:11434/v1"
)


def invoke(system_prompt: str, user_prompt: str, node: str) -> Dict[str, Any]:
    messages = build_messages(system_prompt, user_prompt)
    return client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        stream=False,
        name=f"qwen-llm-{node}"
    )


def invoke_structured(system_prompt: str, user_prompt: str, result_class: Any, node: str) -> Dict[str, Any]:
    messages = build_messages(system_prompt, user_prompt)
    return client.chat.completions.parse(
        model=MODEL,
        messages=messages,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        response_format=result_class,
        name=f"qwen-llm-{node}"
    )


def build_messages(system_prompt: str, user_prompt: str) -> List[Dict[str, str]]:
    """
    Builds a list of messages for the GPT model based on the provided text.
    """
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
