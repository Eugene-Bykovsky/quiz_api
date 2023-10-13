[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Проект "API для викторин"

Это репозиторий, содержащий код и инструкции для запуска API-сервиса на базе Python, используя FastAPI и PostgreSQL. Сервис позволяет получать случайные вопросы для викторин через REST API и сохранять их в базе данных.

## Инструкции по сборке и запуску

Для запуска сервиса необходимо выполнить в корневой директории команду(где находится файл docker-compose.yml):

```bash
docker-compose up -d
```


## Пример запроса к REST API
Для получения случайного вопроса для викторины необходимо выполнить POST запрос на http://127.0.0.1:8000/quiz/ с телом запроса в формате JSON. Пример запроса с использованием curl:

Тело запроса в формате JSON:
```bash
{
    "questions_num": 1
}
```

Ответ будет содержать вопрос в формате JSON, например:
```bash
{
  "id": 1,
  "question_text": "What is the capital of France?",
  "answer_text": "Paris",
  "created_at": "2023-10-13T12:34:56"
}
```

## Стек технологи

Проект разработан с использованием следующего стека технологий:

1. FastAPI
2. Postgres
3. SqlAalchemy
4. Docker
