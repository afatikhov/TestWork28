# Quotes Parser

## Описание проекта

Проект представляет собой асинхронное веб-приложение на FastAPI, которое позволяет парсить цитаты с выбранного сайта и сохранять их в MongoDB с последующей возможностью фильтрации по автору и тегам. Для фоновых задач используется Celery с брокером Redis. Проект упакован в Docker с поддержкой docker-compose для удобного развёртывания.

Для работы Celery реализован синхонный репозиторий mongo, так как он не поддерживает асинхронные функции. Для работы /quotes реализован асинхронный репозиторий монго который работает с fastapi.

### Функциональные возможности

#### POST /parse-quotes-task

Запускает Celery-задачу по скрапингу сайта.

Сохраняет все цитаты в MongoDB (каждая цитата — отдельный документ).

Возвращает task_id запущенной задачи.

Логирует процесс сохранения цитат.

#### GET /quotes

Извлекает цитаты из MongoDB.

Поддерживает фильтрацию по author и/или tags через параметры запроса.

Возвращает специальный ответ при отсутствии цитат по заданным фильтрам(Ошибка 404).

Структура проекта

├── Dockerfile
├── docker-compose.yaml
├── logs/
│   └── quotes_parser.log
├── mongo_data/
├── redis_data/
├── requirements.txt
└── src/
    ├── main.py
    ├── config.py
    ├── logger.py
    ├── schemas.py
    ├── services/
    │   ├── celery_worker.py
    │   ├── quotes_service.py
    │   └── web_page_parcer.py
    └── infrastructure/
        ├── db/
        │   └── mongo_db/
        └── rest_api/
            └── routers/

### Установка и запуск

#### 1. Запуск всех сервисов

docker-compose up -d

Сервисы, которые будут запущены:

FastAPI (порт 8000)

MongoDB (порт 27017)

Redis (порт 6379)

Celery worker

#### 2. Проверка работы

Документация(Swagger) FastAPI доступна по: http://localhost:8035/docs

Логи Celery пишутся в файл: logs/quotes_parser.log

#### 3. Примеры запросов

POST /parse-quotes-task

Request: {
  "page_url": "https://quotes.toscrape.com/"
}
Response: { "task_id": "<celery_task_id>" }

GET /quotes

GET /quotes?author=Albert%20Einstein&tags=life

Возвращает список цитат с указанным автором и тегом.

### Технологии

Python 3.12

FastAPI

Celery

Redis

MongoDB

Docker / Docker Compose

Логирование

#### Примечания

Каждая цитата хранится в MongoDB в документе с полями:

author: string

quote: string

tags: array of strings

created_at: datetime

Redis используется как брокер сообщений для Celery.

MongoDB данные хранятся в mongo_data/, Redis данные в redis_data/.

Логирование данных на данный момент предполагает только чтение файла, также было бы полезно добавить loki + grafana для более удобного мониторинга.


## Вывод

Данный проект демонстрирует полный цикл работы асинхронного веб-приложения: от получения данных с внешнего сайта до их сохранения, фильтрации и последующего использования. Благодаря связке FastAPI + Celery + Redis + MongoDB обеспечивается высокая производительность, масштабируемость и надёжность.

Использование Docker и docker-compose упрощает развёртывание и настройкy.

Проект можно использовать как основу для более сложных систем парсинга, аналитики и обработки данных.
