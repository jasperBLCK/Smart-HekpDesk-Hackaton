FROM python:3.11

WORKDIR /app

# Копируем и устанавливаем зависимости
COPY app/requirements.txt .
RUN pip install -r requirements.txt

# Копируем весь проект
COPY . .

# Запускаем приложение
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
