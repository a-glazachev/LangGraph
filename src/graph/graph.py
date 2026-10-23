"""
Module: graph/graph.py
Description:
    This module is responsible for the graph construction
"""
import uuid

from langfuse import observe, propagate_attributes
from langgraph.constants import START, END
from langgraph.graph import StateGraph

from src.graph.nodes import strategist, copywriter, editor, publisher
from src.graph.state import State


@observe(name="graph-running")
def run_graph(topic: str, task: str):
    session_id = uuid.uuid1()
    with propagate_attributes(session_id="smm-agents-run-" + str(session_id)):
        graph = StateGraph(State)

        graph.add_node(strategist)
        graph.add_node(copywriter)
        graph.add_node(editor)
        graph.add_node(publisher)

        graph.add_edge(START, "strategist")
        graph.add_edge("strategist", "copywriter")
        graph.add_edge("copywriter", "editor")
        graph.add_edge("publisher", END)

        graph = graph.compile()

        state = {
            "topic": topic,
            "task": task,
        }
        config = {
            "recursion_limit": 25,
        }

        return graph.invoke(state, config=config)
