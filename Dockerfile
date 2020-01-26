FROM python:3.7.6-alpine

ADD requirements.txt /
RUN pip install -r requirements.txt

COPY settings.py main.py utils.py /

ENTRYPOINT ["python", "-u", "./main.py"]