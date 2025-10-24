FROM python:3.10
WORKDIR /app

COPY Requirements.txt /app
RUN pip install --upgrade pip && pip install --no-cache-dir -r Requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]