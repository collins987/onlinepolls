FROM python:3.11-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /code/

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
