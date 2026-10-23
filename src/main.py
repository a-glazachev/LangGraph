"""
Module: main.py
Description: 
    This module demonstrates how to use LangGraph
"""

import logging

from dotenv import load_dotenv

from src.config.logger import init_logger
from src.graph.graph import run_graph
from langfuse import get_client

load_dotenv()

langfuse = get_client()

init_logger()
log = logging.getLogger("main")

if __name__ == "__main__":
    topic = "Сеть датацентров, распределенных по РФ"
    # topic = "Сеть фитнес центров на северном полисе"
    task = "Сформировать контент-план на неделю. План должен содержать не менее 3х постов"

    result = run_graph(topic, task)

    log.info("Result state")
    log.info(". topic: %s", result.get('topic'))
    log.info(". task: %s", result.get('task'))
    log.info(". spec:\n%s", result.get('spec'))
    log.info(". posts:\n%s", result.get('posts'))
    log.info(". texts:\n%s", result.get('texts'))
    log.info(". editor_decision: %s", result.get('editor_decision'))
    log.info(". editor_returns: %s", result.get('editor_returns'))

    langfuse.shutdown()