# FROM python:3

# LABEL Edwin Cruz "edwincruz255@gmail.com"

# RUN apt-get update -y && \
#     apt-get install -y python3 python-dev python3-dev \
#      build-essential libssl-dev libffi-dev \
#      libxml2-dev libxslt1-dev zlib1g-dev \
#      python-pip unixodbc-dev python3-flask

# COPY ./requirements.txt /app/requirements.txt

# WORKDIR /app

# # RUN pip3 install numpy
# RUN pip3 install -r requirements.txt

# COPY . /app

# ENTRYPOINT [ "python" ]

# CMD [ "app.py" ]

# https://github.com/ECruz25/cross-entropy-services

FROM ubuntu

RUN apt-get update && \
    apt-get install python3 python3-pip python3-flask python3.6-dev \
    unixodbc-dev libpq-dev pkg-config libcairo2-dev libglib2.0-dev \
    build-essential libssl-dev libffi-dev libgirepository1.0-dev\
    libxml2-dev libxslt1-dev zlib1g-dev libcairo2 \
    python-pip -y

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]

