"""
Module: graph/state.py
Description:
    This module is responsible for graph state
"""

from typing_extensions import TypedDict

from src.graph.editor_desicion import EditorDecision


# graph stage
class State(TypedDict):
    topic: str
    """Бизнес-ниша"""
    task: str
    """Описание задачи"""
    spec: str
    """ТЗ стратега"""
    posts: str
    """Посты копирайтера"""
    texts: str
    """Тексты контент-менеджера"""
    editor_decision: EditorDecision
    """Решение редактора"""
    editor_returns: int
    "Number of returns from the editor"
