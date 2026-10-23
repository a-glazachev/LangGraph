"""
Module: graph/nodes.py
Description:
    This module is responsible for graph nodes
"""
import logging

from langfuse import observe
from langgraph.types import Command

from src.graph.editor_desicion import EditorDecision
from src.graph.state import State
from src.model import llm_local
from src.model import llm_remote

MAX_EDITOR_RETURNS = 3

s_log = logging.getLogger("strategist")
c_log = logging.getLogger("copywriter")
e_log = logging.getLogger("editor")
p_log = logging.getLogger("publisher")


# strategist node
@observe(name="strategist", as_type="agent")
def strategist(state: State) -> dict:
    system_prompt = """
            Ты стратег. Ты анализируешь бизнес-нишу, целевую аудиторию и генерируешь сетку контент-плана с темами и форматами в виде ТЗ для копирайтера.
            """
    user_prompt = f"""
            Бизнес-ниша: {state['topic']}
            Задача: {state['task']}
            """

    s_log.info("system_prompt %s", system_prompt)
    s_log.info("user_prompt %s", user_prompt)

    response = llm_remote.invoke(system_prompt, user_prompt, "strategist")

    if len(response.choices) > 0:
        content = response.choices[0].message.content
        s_log.info("Spec\n%s", content)
    else:
        s_log.info("There is no answer from LLM")
        raise

    return {
        "spec": content
    }


# copywriter node
@observe(name="copywriter", as_type="agent")
def copywriter(state: State) -> dict:
    system_prompt = """
            Ты копирайтер. Ты пишешь креативные тексты постов, строго опираясь на ТЗ.
            Учитывай правки редактора, если предоставлены.
            В ответ добавляй только финальные тексты постов для издателя.
            """
    user_prompt = f"""
            ТЗ:\n{state['spec']}            
            
            {
                'Тексты постов (требуют правок):\n' + state['posts'] + 
                '\n\nПравки редактора:\n' + state['editor_decision'].details if state.get('editor_decision') and not state.get('editor_decision').approved else ''
            }            
            """

    c_log.info("system_prompt %s", system_prompt)
    c_log.info("user_prompt %s", user_prompt)

    response = llm_local.invoke(system_prompt, user_prompt, "copywriter")

    if len(response.choices) > 0:
        content = response.choices[0].message.content
        c_log.info("Posts\n%s", content)
    else:
        c_log.info("There is no answer from LLM")
        raise

    return {
        "posts": content
    }


# editor node
@observe(name="editor", as_type="agent")
def editor(state: State) -> Command:
    system_prompt = """
            Ты редактор. Ты проверяешь тексты Копирайтера на стилистику, ошибки, наличие призывов к действию (CTA) и соответствие контент-плану (ТЗ).
            Сам правки не вноси, только отправляй замечания копирайтеру.
            Результат оформляй только в виде json.
            Поле approved - результата проверки: true - пройдена проверка не требуется правок, false - требуются правки копирайтером. 
            Поле details - текстовые пояснения для копирайтера.
            """
    user_prompt = f"""
            ТЗ:\n{state['spec']}
            
            Тексты Копирайтера:\n{state['posts']}
            """

    e_log.info("system_prompt %s", system_prompt)
    e_log.info("user_prompt %s", user_prompt)

    response = llm_remote.invoke_structured(system_prompt, user_prompt, EditorDecision, "editor")

    if len(response.choices) > 0:
        decision = response.choices[0].message.parsed
        e_log.info("Editor decision\n%s", decision)
    else:
        e_log.info("There is no answer from LLM")
        raise

    # conditional return
    returns = state.get('editor_returns', 0)
    if decision.approved:
        e_log.info("Move to the publisher")
        goto = 'publisher'
    else:
        if returns > MAX_EDITOR_RETURNS:
            e_log.info("Number of attempts exceeded, max attempts: %s", MAX_EDITOR_RETURNS)
            goto = 'publisher'
        else:
            e_log.info("Return to the copywriter, attempt %s from %s", returns, MAX_EDITOR_RETURNS)
            returns += 1
            goto = 'copywriter'
    return Command(
        update={
            "editor_decision": decision,
            "editor_returns": returns
        },
        goto=goto
    )


# publisher node
@observe(name="publisher", as_type="agent")
def publisher(state: State) -> dict:
    system_prompt = """
            Ты Паблишер/Контент-менеджер. Ты финализируешь тексты от копирайтера, добавляешь нужные хештеги, эмодзи и адаптируешь форматирование под соцсеть Max.
            Сохрани число и структуру постов от копирайтера.
            В ответ добавляй только финальные тексты постов для публикации.
            """
    user_prompt = f"""
            Тексты Копирайтера:\n{state['posts']}
            """

    p_log.info("system_prompt %s", system_prompt)
    p_log.info("user_prompt %s", user_prompt)

    response = llm_local.invoke(system_prompt, user_prompt, "publisher")

    if len(response.choices) > 0:
        content = response.choices[0].message.content
        p_log.info("Texts\n%s", content)
    else:
        p_log.info("There is no answer from LLM")
        raise

    return {
        "texts": content
    }
