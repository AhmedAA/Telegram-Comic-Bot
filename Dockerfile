FROM python:3.5.1

RUN mkdir /home/docker-py

COPY requirements.txt /home/docker-py/requirements.txt
COPY keys/ /home/docker-py/keys/
COPY telegram-comic-bot /home/docker-py/telegram-comic-bot/

WORKDIR /home/docker-py/

RUN pip install -r requirements.txt && python telegram-comic-bot/main.py keys/token.txt
