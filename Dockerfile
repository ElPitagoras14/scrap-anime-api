FROM python:3.12

RUN apt update && apt upgrade -y
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt install ./google-chrome-stable_current_amd64.deb -y

WORKDIR /app

COPY src /app/src
COPY Dockerfile /app
COPY requirements.txt /app
COPY docker-compose.yaml /app

ENV IN_DOCKER=true

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["sh", "-c", "cd src && python main.py"]
