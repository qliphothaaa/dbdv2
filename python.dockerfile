FROM python:3.7

COPY ./requirements.txt /tmp/requirements.txt
EXPOSE 8090
RUN apt-get update  \
    && apt-get install -y chromium \
    && apt-get install -y tesseract-ocr \
    && apt-get install -y libgconf-2-4 \
    && pip3 install -r /tmp/requirements.txt && rm /tmp/requirements.txt

CMD ["/bin/bash"]
