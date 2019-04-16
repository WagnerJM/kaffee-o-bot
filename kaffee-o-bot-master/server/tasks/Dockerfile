FROM python:3.6

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

#ENTRYPOINT celery -A tasks worker  --loglevel=info
