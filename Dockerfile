FROM python:3.5.1

RUN mkdir /home/docker-py

COPY /src /home/docker-py
RUN pip install -r /home/docker-py/requirements.txt

WORKDIR /home/docker-py