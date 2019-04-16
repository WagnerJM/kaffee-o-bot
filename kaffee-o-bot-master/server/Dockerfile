# base image
FROM python:3.6.5-slim

RUN mkdir /server

WORKDIR /server

ADD . .

# set working directory

EXPOSE 5000

# add and install requirements
COPY ./requirements.txt /server/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY . /server
#RUN export PYTHONPATH="$PYTHONPATH:/server"
RUN export PYTHONPATH="$PYTHONPATH:/server/app"


#FOR DEV
#CMD ["flask", "run", "--host=0.0.0.0"]

#CMD ["gunicorn", "-w", "2", "-b", ":8000", "wsgi:app"]
