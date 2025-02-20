# Task Manager Service

## Использование через Docker

1. Клонирование репозитория

git clone https://github.com/mitisit/task-manager.git
cd task-manager

2. Запуск с использованием Docker Compose

docker-compose up --build

Документация API

После запуска сервис доступен по адресу: http://localhost:8000

Документация OpenAPI: http://localhost:8000/docs

## Использование без докера

1. Установите зависимостости с помощью uv
```sh uv venv && uv sync && source .venv/bin/activate```
2. Установите rabbitmq,redis с помошью пакетного менежера вашего дистрибутива
3. Для запуска сервера ```sh fastapi dev main:app```
4. Для запуска воркера ```python -m app.worker.main```
