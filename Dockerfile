FROM python:3.5.1

ADD /requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

ADD /src /code
ADD /keys /keys
WORKDIR /code