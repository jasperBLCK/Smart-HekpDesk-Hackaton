# 🦇 Project

<div align="center">

![Project](https://img.shields.io/badge/Project-blue?style=for-the-badge&logo=project)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

**Система управления задачами для Академии АХО**

[🚀 Запуск](#-быстрый-старт) • [🐳 Docker](#-docker) • [📱 Интерфейс](#-веб-интерфейс)

</div>

---

## О проекте

Project - система для управления задачами и пользователями в Академии АХО.

### Возможности

- Аутентификация пользователей
- Управление пользователями и ролями
- Создание и отслеживание задач
- Веб-интерфейс
- Docker для развертывания
- API документация

## Запуск

### Docker

```bash
# Windows
start.bat

# Linux/Mac
docker-compose up --build
```

### Локально

```bash
pip install -r app/requirements.txt

# Создать .env
DATABASE_URL=postgresql+psycopg2://postgres:***REMOVED***@localhost:5432/HelpDesk
JWT_SECRET_KEY=your-secure-secret-key

python -m uvicorn app.main:app --reload
```

### Доступ

- Веб-интерфейс: http://localhost:8000
- API документация: http://localhost:8000/docs

## Веб-интерфейс

- Главная страница: http://localhost:8000
- Аутентификация: http://localhost:8000/auth
- Пользователи: http://localhost:8000/users
- Задачи: http://localhost:8000/tasks

## API

### Аутентификация
- POST `/auth/register` - регистрация
- POST `/auth/login` - вход
- POST `/auth/logout` - выход

### Пользователи
- GET `/api/users` - список пользователей
- POST `/api/users` - создать пользователя
- GET `/api/users/{id}` - получить пользователя
- PUT `/api/users/{id}` - обновить пользователя

### Задачи
- GET `/api/tasks` - список задач
- POST `/api/tasks` - создать задачу
- GET `/api/tasks/{id}` - получить задачу
- PUT `/api/tasks/{id}` - обновить задачу
- DELETE `/api/tasks/{id}` - удалить задачу
- PATCH `/api/tasks/{id}/status` - изменить статус
- PATCH `/api/tasks/{id}/assign` - назначить исполнителя

## Docker

### Запуск

```bash
# Windows
start.bat

# Остановка
stop.bat
```

### Контейнеры

- Веб-приложение на порту 8000
- PostgreSQL на порту 5432

### Настройка

Создать файл `.env`:
```bash
DATABASE_URL=postgresql+psycopg2://postgres:***REMOVED***@localhost:5432/HelpDesk
JWT_SECRET_KEY=your-secure-secret-key
```

## Структура проекта

```
batman_project/
├── Dockerfile
├── docker-compose.yml
├── start.bat
├── stop.bat
├── app/
│   ├── main.py
│   ├── database.py
│   ├── requirements.txt
│   ├── auth/
│   │   ├── models.py
│   │   ├── routes.py
│   │   ├── schemas.py
│   │   └── hash.py
│   ├── users/
│   │   ├── models.py
│   │   ├── routes.py
│   │   └── schemas.py
│   ├── tasks/
│   │   ├── models.py
│   │   ├── routes.py
│   │   └── schemas.py
│   ├── templates/
│   │   ├── index.html
│   │   ├── auth.html
│   │   ├── users.html
│   │   └── tasks.html
│   └── static/
│       ├── css/styles.css
│       └── js/api.js
└── README.md
```

## Технологии

- FastAPI + SQLAlchemy + PostgreSQL
- HTML5 + CSS3 + JavaScript
- Jinja2 шаблоны
- Docker

## 🔧 Установка зависимостей

```bash
# Установить зависимости
pip install -r app/requirements.txt
```

## 📝 Примеры использования

### Создание пользователя
```bash
curl -X POST "http://localhost:8000/api/users" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "user1",
    "username": "john_doe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "phone": "+1234567890",
    "role": "Электрик",
    "department": "Технический отдел",
    "is_active": true
  }'
```

### Создание задачи
```bash
curl -X POST "http://localhost:8000/api/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Ремонт освещения",
    "description": "Заменить лампы в коридоре",
    "category": "Электрика",
    "status": "Новая",
    "priority": "High",
    "location_id": "Коридор 1",
    "created_by": "user1"
  }'
```

## 🎯 Статусы задач

- **Новая** - только что созданная задача
- **В работе** - задача в процессе выполнения
- **Выполнена** - задача завершена
- **Отменена** - задача отменена

## 🏷 Приоритеты задач

- **Critical** - критический приоритет
- **High** - высокий приоритет
- **Medium** - средний приоритет
- **Low** - низкий приоритет

## 👥 Роли пользователей

- **Руководитель отдела** - управление отделом
- **Сервис-менеджер** - управление сервисами
- **Электрик** - электрические работы
- **Энергетик** - энергетические системы
- **Специалист по отоплению** - системы отопления

---

## 📚 Дополнительная документация

- **[📖 Полная документация](DOCUMENTATION.md)** - Подробное описание всех возможностей
- **[🐳 Docker команды](docker-commands.md)** - Все команды для работы с Docker
- **[📚 API документация](http://localhost:8000/docs)** - Интерактивная документация API



*Разработано для Академии АХО*
