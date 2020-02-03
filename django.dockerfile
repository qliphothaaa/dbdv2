FROM python:3.7

COPY ./requirements_django.txt /tmp/requirements_django.txt

RUN pip3 install -r /tmp/requirements_django.txt && rm /tmp/requirements_django.txt



