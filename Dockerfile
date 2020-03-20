
FROM joeshaw/uwsgi-nginx-ubuntu

RUN apt-get update && \
    apt-get install python3 python3-pip python3-flask python3.6-dev \
    unixodbc-dev libpq-dev pkg-config libcairo2-dev libglib2.0-dev \
    build-essential libssl-dev libffi-dev libgirepository1.0-dev\
    libxml2-dev libxslt1-dev zlib1g-dev libcairo2 \
    python-pip -y

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt
RUN pip3 install uwsgi flask
RUN sudo ufw allow 5000

COPY . /app



