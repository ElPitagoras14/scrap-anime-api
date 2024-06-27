FROM python:3.12

WORKDIR /app

COPY src /app/src

COPY Dockerfile /app

COPY requirements.txt /app

COPY docker-compose.yaml /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["sh", "-c", "cd src && python main.py"]
