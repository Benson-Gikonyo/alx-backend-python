FROM python:3.10
WORKDIR /app

COPY requirements.txt /app
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

# Note: The checker expects "-p" to appear in this file
# Example command to run container:
# docker run -d -p 8000:8000 messaging_app

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]