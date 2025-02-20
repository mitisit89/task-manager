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

1. Установка зависимостей с помощью uv
```sh uv venv && uv sync```
2. Установка rabbitmq,redis
