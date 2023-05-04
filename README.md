# Food Calculate

## Запуск проекта для разработки

- `python -m venv venv` - создание виртуального окружения
- `venv\Scripts\activate ` - войти в виртуальное окружение
- `pip install -r requirements.txt` - установка зависимостей
- `docker-compose up -d` - запустить postgreSQL сервис в Docker
- `python manage.py migrate` - примененить миграции
- `python manage.py runserver` - запустить сервер для разработки на http://127.0.0.1:8000