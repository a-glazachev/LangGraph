# OTUS. LangGraph

Небольшой проект для изучения LangGraph

Модели:

- llm локальная - qwen3:4b (через ollama)
- llm удаленная - yandexgpt-lite

## Что внутри

- `src/main.py` — основной модуль (запуск графа)
- `src/config/logger.py` — настройка логгирования
- `src/graph/editor_decision.py` — класс решения редактора
- `src/graph/graph.py` — сборка графа целиком
- `src/graph/nodes.py` — узлы графа
- `src/graph/state.py` — состояние графа
- `src/model/llm_local.py` — локальная модель на ollama
- `src/model/llm_remote.py` — удаленная модель yandexgpt-lite
- `src/model/variables.py` — переменные для yandexgpt-lite

## Настройка

1. Установите зависимости:

```bash
uv sync
```

2. Создайте файл `.env` в корне проекта (на основе .env.example):

```env
YC_API_KEY=your_api_key
YC_FOLDER_ID=your_folder_id

LANGFUSE_SECRET_KEY=your_secret_key
LANGFUSE_PUBLIC_KEY=your_public_key
LANGFUSE_BASE_URL=your_langfuse_url
```

3. Запустите langfuse:

```bash
git clone https://github.com/langfuse/langfuse.git
cd langfuse
docker compose up
```

4. Активируйте виртуальное окружение:

```bash
source .venv/bin/activate
```

## Запуск

```bash
python src/main.py
```

## Результаты

Web версия langfuse: http://localhost:3000/

В консоле отображаются:

- лог выполнения графа (для каждого узла графа свой логгер)
- выводятся входные/выходные параметры для каждого из узлов
- в конце отображается итоговое состояние графа
