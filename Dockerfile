FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7


RUN apk --update add python3 python3-pip python3-flask python3.6-dev \
    unixodbc-dev libpq-dev pkg-config libcairo2-dev libglib2.0-dev \
    build-essential libssl-dev libffi-dev libgirepository1.0-dev\
    libxml2-dev libxslt1-dev zlib1g-dev libcairo2 \
    python-pip -y

ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static
COPY ./requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt



